from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import uuid, os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, AutoMaker, AutoModel, AutoModelImage, User

# Imports for oauth
from flask import session as login_session
import random, string, itertools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests



app = Flask(__name__)

# App configuration intended for image uploads
app.config['UPLOAD_FOLDER'] = 'static/images/models/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg'])

# For a given file for upload, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Luxury Rides App"



#Connect to Database and create database session
engine = create_engine('sqlite:///luxuryridescatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Create route for Google+ sign in
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
      user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 10px;-webkit-border-radius: 10px;-moz-border-radius: 10px;"> '
    #flash("you are now logged in as %s" % login_session['username'])
    return output

# Create route for Google+ sign out
@app.route("/gdisconnect")
def gdisconnect():
  # Only disconnect a connected user
  credentials = login_session.get('credentials')
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Execute HTTP GET request to revoke current token
  access_token = credentials.access_token
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]

  if result['status'] == '200':
    # Reset the user's session
    del login_session['credentials']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return redirect(url_for('showCatalogs'))
  else:
    # For whatever reason, the given token was invalid
    response = make_response(json.dumps('Failed to revoke token for the given user.'), 400)
    response.headers['Content-Type'] = 'application/json'
    return response



# Home page, show all auto makers
@app.route('/')
@app.route('/catalog')
def showCatalogs():
	auto_makers = session.query(AutoMaker).order_by(asc(AutoMaker.id))
	return render_template('public_catalog.html', auto_makers = auto_makers, login_session = login_session)


# Auto maker page, show all models for a specific auto maker
@app.route('/catalog/<int:auto_maker_id>')
@app.route('/catalog/<int:auto_maker_id>/models')
def showCatalogModels(auto_maker_id):
	auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
	models = session.query(AutoModel).filter_by(auto_maker_id = auto_maker_id).all()
	return render_template('public_models.html', models = models, auto_maker = auto_maker, login_session = login_session)


# Model page, show a specific model for a specific auto maker
@app.route('/catalog/<int:auto_maker_id>/models/<int:auto_model_id>')
def showModel(auto_maker_id, auto_model_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    model = session.query(AutoModel).filter_by(id = auto_model_id).one()
    model_images = session.query(AutoModelImage).filter_by(auto_model_id = auto_model_id).all()
    author = getUserInfo(model.user_id)
    return render_template('public_model.html', model = model, model_images = model_images, auto_maker = auto_maker, author = author, login_session = login_session)


# Create new model page
@app.route('/catalog/<int:auto_maker_id>/models/new', methods=['GET','POST'])
def newCatalogModel(auto_maker_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['thumbnail_picture']
        if file and allowed_file(file.filename):
            extension = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4())+extension
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "<script>function myFunction() {alert('Thumbnail picture in jpg/jpeg format required');}</script><body onload='myFunction()''>"
        newCatalogModel = (AutoModel(name = request.form['name'], description = request.form['description'],
            thumbnail_picture = '../../'+filepath, auto_maker_id = auto_maker_id,
            user_id = login_session['user_id']))
        session.add(newCatalogModel)
        session.commit()
        flash('New Model %s Successfully Created' % (newCatalogModel.name))
        return redirect(url_for('showCatalogModels', auto_maker_id = auto_maker_id))
    else:
        return render_template('new_model.html', auto_maker = auto_maker, login_session = login_session)


# Edit model page
@app.route('/catalog/<int:auto_maker_id>/models/<int:auto_model_id>/edit', methods=['GET','POST'])
def editCatalogModel(auto_maker_id, auto_model_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    modelToEdit = session.query(AutoModel).filter_by(id = auto_model_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            modelToEdit.name = request.form['name']
        if request.form['description']:
            modelToEdit.description = request.form['description']
        if request.files['thumbnail_picture']:
            file1 = request.files['thumbnail_picture']
            if allowed_file(file1.filename):
                extension1 = os.path.splitext(file1.filename)[1]
                filename1 = str(uuid.uuid4())+extension1
                filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            else:
                return "<script>function myFunction() {alert('Thumbnail picture only in jpg/jpeg format');}</script><body onload='myFunction()''>"
            modelToEdit.thumbnail_picture = '../../'+filepath1
        if request.files['new_model_image']:
            file2 = request.files['new_model_image']
            if allowed_file(file2.filename):
                extension2 = os.path.splitext(file2.filename)[1]
                filename2 = str(uuid.uuid4())+extension2
                filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            else:
                return "<script>function myFunction() {alert('Model image only in jpg/jpeg format');}</script><body onload='myFunction()''>"
            newModelImage = (AutoModelImage(image_url = '../../'+filepath2, auto_maker_id = auto_maker_id, 
                auto_model_id = auto_model_id, user_id = login_session['user_id']))
            session.add(newModelImage)
        
        session.add(modelToEdit)
        session.commit() 
        flash('Model %s Successfully Edited' % (modelToEdit.name))
        return redirect(url_for('showCatalogModels', auto_maker_id = auto_maker_id))
    else:
        return render_template('edit_model.html', auto_maker_id = auto_maker_id, auto_model_id = auto_model_id, model = modelToEdit, login_session = login_session)


# Delete model page
@app.route('/catalog/<int:auto_maker_id>/models/<int:auto_model_id>/delete', methods=['GET','POST'])
def deleteCatalogModel(auto_maker_id, auto_model_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    modelToDelete = session.query(AutoModel).filter_by(id = auto_model_id).one()
    deletedModelName = modelToDelete.name
    if 'username' not in login_session:
        return redirect('/login')
    # Restrict delete to only models created by the current logged in user
    if modelToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this model');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(modelToDelete)
        session.commit()
        flash('Model %s Successfully Deleted' % deletedModelName)
        return redirect(url_for('showCatalogModels', auto_maker_id = auto_maker_id))
    else:
        return render_template('delete_model.html', auto_maker_id = auto_maker_id, auto_model_id = auto_model_id, model = modelToDelete, login_session = login_session)



# JSON APIs to view Catalog Information
# Show all auto makers
@app.route('/catalog/JSON')
def autoMakersJSON():
    auto_makers = session.query(AutoMaker).all()
    return jsonify(autoMakers = [a.serialize for a in auto_makers])

# Show specific auto maker
@app.route('/catalog/<int:auto_maker_id>/JSON')
def autoMakerJSON(auto_maker_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    return jsonify(autoMaker = auto_maker.serialize)

# Show all auto models of all auto makers
@app.route('/catalog/models/JSON')
def autoModelsJSON():
    auto_models = session.query(AutoModel).all()
    return jsonify(autoModels = [a.serialize for a in auto_models])

# Show all models for specific auto maker
@app.route('/catalog/<int:auto_maker_id>/models/JSON')
def autoMakerModelsJSON(auto_maker_id):
    models = session.query(AutoModel).filter_by(auto_maker_id = auto_maker_id).all()
    return jsonify(autoMakerModels=[m.serialize for m in models])

# Show specific model
@app.route('/catalog/<int:auto_maker_id>/models/<int:auto_model_id>/JSON')
def autoMakerModelJSON(auto_maker_id, auto_model_id):
    model = session.query(AutoModel).filter_by(id = auto_model_id).one()
    return jsonify(autoMakerModel=model.serialize)

# Show all model images
@app.route('/catalog/models/images/JSON')
def autoModelsImagesJSON():
    auto_models_images = session.query(AutoModelImage).all()
    return jsonify(autoModelsImages = [a.serialize for a in auto_models_images])



# XML APIs to view Catalog Information
# Show all auto makers
@app.route('/catalog/XML')
def autoMakersXML():
    auto_makers = session.query(AutoMaker).all()
    auto_makers_list = ([a.serialize for a in auto_makers])

    autoMakers = ET.Element("autoMakers")

    for make in auto_makers_list:
        autoMaker = ET.SubElement(autoMakers,"autoMaker")
        for k, v in make.iteritems():
            k = ET.SubElement(autoMaker, k)
            k.text = str(v)

    tree = ET.tostring(autoMakers, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)

# Show specific auto maker
@app.route('/catalog/<int:auto_maker_id>/XML')
def autoMakerXML(auto_maker_id):
    auto_maker = session.query(AutoMaker).filter_by(id = auto_maker_id).one()
    auto_maker_dict = auto_maker.serialize

    autoMaker = ET.Element("autoMaker")
    for k, v in auto_maker_dict.iteritems():
        k = ET.SubElement(autoMaker, k)
        k.text = str(v)

    tree = ET.tostring(autoMaker, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)

# Show all auto models of all auto makers
@app.route('/catalog/models/XML')
def autoModelsXML():
    auto_models = session.query(AutoModel).all()
    auto_models_list = ([a.serialize for a in auto_models])

    autoModels = ET.Element("autoModels")

    for model in auto_models_list:
        autoModel = ET.SubElement(autoModels,"autoModel")
        for k, v in model.iteritems():
            k = ET.SubElement(autoModel, k)
            k.text = str(v)

    tree = ET.tostring(autoModels, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)

# Show all models for specific auto maker
@app.route('/catalog/<int:auto_maker_id>/models/XML')
def autoMakerModelsXML(auto_maker_id):
    models = session.query(AutoModel).filter_by(auto_maker_id = auto_maker_id).all()
    auto_maker_models_list = ([m.serialize for m in models])

    autoMakerModels = ET.Element("autoMakerModels")

    for model in auto_maker_models_list:
        autoModel = ET.SubElement(autoMakerModels,"autoModel")
        for k, v in model.iteritems():
            k = ET.SubElement(autoModel, k)
            k.text = str(v)

    tree = ET.tostring(autoMakerModels, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)

# Show specific model
@app.route('/catalog/<int:auto_maker_id>/models/<int:auto_model_id>/XML')
def autoMakerModelXML(auto_maker_id, auto_model_id):
    model = session.query(AutoModel).filter_by(id = auto_model_id).one()
    auto_maker_model_dict = model.serialize

    autoModel = ET.Element("autoModel")
    for k, v in auto_maker_model_dict.iteritems():
        k = ET.SubElement(autoModel, k)
        k.text = str(v)

    tree = ET.tostring(autoModel, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)

# Show all model images
@app.route('/catalog/models/images/XML')
def autoModelsImagesXML():
    auto_models_images = session.query(AutoModelImage).all()
    auto_models_images_list = ([a.serialize for a in auto_models_images])

    autoModelsImages = ET.Element("autoModelsImages")

    for model_image in auto_models_images_list:
        autoModel = ET.SubElement(autoModelsImages,"autoModel")
        for k, v in model_image.iteritems():
            k = ET.SubElement(autoModel, k)
            k.text = str(v)

    tree = ET.tostring(autoModelsImages, 'utf-8')
    reparsed_tree = minidom.parseString(tree)
    xml_output = reparsed_tree.toprettyxml(indent="  ")

    return render_template('xml_view.html', xml_output = xml_output)


#User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
