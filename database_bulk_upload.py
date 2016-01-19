from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, AutoMaker, AutoModel, AutoModelImage, User

engine = create_engine('sqlite:///luxuryridescatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create admin user
Admin = User(name="Site Admin", email="nonsoogbonna@gmail.com",
             picture="../../static/images/admin/profile-image.jpg")
session.add(Admin)
session.commit()



# Catalog for Maserati
auto_maker1 = AutoMaker(user_id=1, name="Maserati",
                        description=("A hundred years since it was founded, Maserati is "
                           "still staying true to its values by continuing to build cars "
                           "where outstanding sporting performance is always combined "
                           "with exclusive quality, comfort, luxurious interiors and "
                           "elegant lines."),
                        thumbnail_picture="../../static/images/models/maserati-thumbnail.jpg",
                        banner_picture="../../static/images/models/maserati-banner.jpg")

session.add(auto_maker1)
session.commit()

auto_model1 = AutoModel(user_id=1, name="Ghibli",
                     description=("Sculpted forms and well-defined volumes connected by clean "
                        "lines that create movement: the Ghibli captures the attention with "
                        "its emphasis on sporty glamour and, just like the first Ghibli "
                        "launched back in 1967, captivates with its strong personality."),
                     thumbnail_picture="../../static/images/models/maserati-ghibli-thumbnail.jpg",
                     auto_maker=auto_maker1)

session.add(auto_model1)
session.commit()

auto_model_image1 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-ghibli-1.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model1)

auto_model_image2 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-ghibli-2.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model1)

auto_model_image3 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-ghibli-3.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model1)

auto_model_image4 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-ghibli-4.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model1)

session.add_all([auto_model_image1, auto_model_image2, auto_model_image3, auto_model_image4])
session.commit()


auto_model2 = AutoModel(user_id=1, name="Quattroporte",
                     description=("The Quattroporte with its 330 hp entry-level engine delivers "
                        "refined luxury paired with an unmistakably sporty personality. This is "
                        "obvious at first glance: Muscular lines and charismatic forms meet "
                        "elegant contours, that envelope a generous interior where in the "
                        "finest traditions of Italian craftsmanship, only the highest quality "
                        "materials are used."),
                     thumbnail_picture="../../static/images/models/maserati-quattroporte-thumbnail.jpg",
                     auto_maker=auto_maker1)

session.add(auto_model2)
session.commit()

auto_model_image5 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-quattroporte-1.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model2)

auto_model_image6 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-quattroporte-2.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model2)

auto_model_image7 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-quattroporte-3.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model2)

auto_model_image8 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-quattroporte-4.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model2)

session.add_all([auto_model_image5, auto_model_image6, auto_model_image7, auto_model_image8])
session.commit()


auto_model3 = AutoModel(user_id=1, name="Granturismo",
                     description=("The Maserati GranTurismo succeeds in combining unrivalled "
                        "class and elegance with uncompromising sports performance like no "
                        "other four-seater car. The external lines exude dynamic tension and "
                        "sporting prowess from every vantage point."),
                     thumbnail_picture="../../static/images/models/maserati-granturismo-thumbnail.jpg",
                     auto_maker=auto_maker1)

session.add(auto_model3)
session.commit()

auto_model_image9 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-granturismo-1.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model3)

auto_model_image10 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-granturismo-2.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model3)

auto_model_image11 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-granturismo-3.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model3)

auto_model_image12 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-granturismo-4.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model3)

session.add_all([auto_model_image9, auto_model_image10, auto_model_image11, auto_model_image12])
session.commit()


auto_model4 = AutoModel(user_id=1, name="Grancabrio",
                     description=("When passion meets freedom the outcome is inevitably unique: "
                        "as the first convertible of the brand to seat four in comfort, the Maserati "
                        "GranCabrio is the start of a major new chapter in its history."),
                     thumbnail_picture="../../static/images/models/maserati-grancabrio-thumbnail.jpg",
                     auto_maker=auto_maker1)

session.add(auto_model4)
session.commit()

auto_model_image13 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-grancabrio-1.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model4)

auto_model_image14 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-grancabrio-2.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model4)

auto_model_image15 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-grancabrio-3.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model4)

auto_model_image16 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/maserati-grancabrio-4.jpg",
                                   auto_maker=auto_maker1,
                                   auto_model=auto_model4)

session.add_all([auto_model_image13, auto_model_image14, auto_model_image15, auto_model_image16])
session.commit()



# Catalog for Aston Martin
auto_maker2 = AutoMaker(user_id=1, name="Aston Martin",
                        description=("Aston Martin takes you on a journey, a voyage of inspiration "
                          "through the world of art, design and craft, to distant lands or "
                          "favourite places, soaking up the character of objects and artefacts, "
                          "materials, colours, textures and forms and translating them into key "
                          "elements of your own car."),
                        thumbnail_picture="../../static/images/models/astonmartin-thumbnail.jpg",
                        banner_picture="../../static/images/models/astonmartin-banner.jpg")

session.add(auto_maker2)
session.commit()

auto_model5 = AutoModel(user_id=1, name="V12 Vantage",
                     description=("The V12 Vantage was an unprecedented engineering achievement. "
                      "Combining a V12 engine with our lightest sports-car in a package of pure "
                      "aggression. An even lighter chassis, an even more powerful engine, an "
                      "even more responsive transmission. "),
                     thumbnail_picture="../../static/images/models/astonmartin-vantage-thumbnail.jpg",
                     auto_maker=auto_maker2)

session.add(auto_model5)
session.commit()

auto_model_image17 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vantage-1.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model5)

auto_model_image18 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vantage-2.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model5)

auto_model_image19 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vantage-3.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model5)

auto_model_image20 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vantage-4.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model5)

session.add_all([auto_model_image17, auto_model_image18, auto_model_image19, auto_model_image20])
session.commit()

auto_model6 = AutoModel(user_id=1, name="DB9",
                     description=("It was an incredible challenge, make a great design even better. "
                      "It took an extraordinary collaborative effort to achieve. It is as timeless "
                      "and elegant as ever. The best DB9 yet."),
                     thumbnail_picture="../../static/images/models/astonmartin-db9-thumbnail.jpg",
                     auto_maker=auto_maker2)

session.add(auto_model6)
session.commit()

auto_model_image21 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-db9-1.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model6)

auto_model_image22 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-db9-2.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model6)

auto_model_image23 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-db9-3.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model6)

auto_model_image24 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-db9-4.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model6)

session.add_all([auto_model_image21, auto_model_image22, auto_model_image23, auto_model_image24])
session.commit()

auto_model7 = AutoModel(user_id=1, name="Rapide S",
                     description=("Rapide S is the worlds most beautiful four door sports car. "
                      "Created with the finest ingredients, conceived with a unique vision, it "
                      "combines sensational sports car performance and supreme refinement in "
                      "one compelling form. "),
                     thumbnail_picture="../../static/images/models/astonmartin-rapides-thumbnail.jpg",
                     auto_maker=auto_maker2)

session.add(auto_model7)
session.commit()

auto_model_image25 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-rapides-1.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model7)

auto_model_image26 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-rapides-2.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model7)

auto_model_image27 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-rapides-3.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model7)

auto_model_image28 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-rapides-4.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model7)

session.add_all([auto_model_image25, auto_model_image26, auto_model_image27, auto_model_image28])
session.commit()

auto_model8 = AutoModel(user_id=1, name="Vanquish",
                     description=("Our mission was to produce the greatest Aston Martin in history, "
                      "a new flagship to lead us into our second century. With the most advanced "
                      "engineering, the most beautiful design and the finest materials, we created "
                      "the ultimate Aston Martin. We created Vanquish."),
                     thumbnail_picture="../../static/images/models/astonmartin-vanquish-thumbnail.jpg",
                     auto_maker=auto_maker2)

session.add(auto_model8)
session.commit()

auto_model_image29 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vanquish-1.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model8)

auto_model_image30 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vanquish-2.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model8)

auto_model_image31 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vanquish-3.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model8)

auto_model_image32 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/astonmartin-vanquish-4.jpg",
                                   auto_maker=auto_maker2,
                                   auto_model=auto_model8)

session.add_all([auto_model_image29, auto_model_image30, auto_model_image31, auto_model_image32])
session.commit()



# Catalog for Lamborghini
auto_maker3 = AutoMaker(user_id=1, name="Lamborghini",
                        description=("Founded in 1963, Automobili Lamborghini is headquartered "
                          "in Sant Agata Bolognese, in Northeastern Italy. There it manufactures "
                          "some of the worlds most sought-after super sports cars. With the "
                          "presentation of the Huracan LP 6104, Lamborghini offers a new "
                          "dimension in luxury super sports cars."),
                        thumbnail_picture="../../static/images/models/lamborghini-thumbnail.jpg",
                        banner_picture="../../static/images/models/lamborghini-banner.jpg")

session.add(auto_maker3)
session.commit()

auto_model9 = AutoModel(user_id=1, name="Huracan",
                     description=("It is like a time machine, Only faster. There is nothing "
                        "from the past the past that rivals the technology of the new Huracan, "
                        "which comes together in a perfect car that seems straight out of "
                        "the future "),
                     thumbnail_picture="../../static/images/models/lamborghini-huracan-thumbnail.jpg",
                     auto_maker=auto_maker3)

session.add(auto_model9)
session.commit()

auto_model_image33 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-huracan-1.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model9)

auto_model_image34 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-huracan-2.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model9)

auto_model_image35 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-huracan-3.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model9)

auto_model_image36 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-huracan-4.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model9)

session.add_all([auto_model_image33, auto_model_image34, auto_model_image35, auto_model_image36])
session.commit()

auto_model10 = AutoModel(user_id=1, name="Aventador",
                     description=("The Aventador with its uncompromising crisp contours is the "
                        "essence of our brand, poured into an extreme, awe inspiring look. "
                        "Eternally different, unmistakably Lamborghini."),
                     thumbnail_picture="../../static/images/models/lamborghini-aventador-thumbnail.jpg",
                     auto_maker=auto_maker3)

session.add(auto_model10)
session.commit()

auto_model_image37 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-aventador-1.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model10)

auto_model_image38 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-aventador-2.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model10)

auto_model_image39 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-aventador-3.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model10)

auto_model_image40 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-aventador-4.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model10)

session.add_all([auto_model_image37, auto_model_image38, auto_model_image39, auto_model_image40])
session.commit()

auto_model11 = AutoModel(user_id=1, name="Veneno",
                     description=("An open racing prototype with an extreme design and breathtaking "
                      "performance. And it is one of the worlds most exclusive automobiles: not "
                      "more than nine units will be built during the course of 2014."),
                     thumbnail_picture="../../static/images/models/lamborghini-veneno-thumbnail.jpg",
                     auto_maker=auto_maker3)

session.add(auto_model11)
session.commit()

auto_model_image41 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-veneno-1.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model11)

auto_model_image42 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-veneno-2.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model11)

auto_model_image43 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-veneno-3.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model11)

auto_model_image44 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-veneno-4.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model11)

session.add_all([auto_model_image41, auto_model_image42, auto_model_image43, auto_model_image44])
session.commit()

auto_model12 = AutoModel(user_id=1, name="Asterion",
                     description=("The glittery Blue Elektra color of the Asterion and the innovative "
                      "lines of its stylish look reflect the technology incorporated into the vehicle. "
                      "Designed by Lamborghini Centro Stile, the Asterion is unmistakably a Lamborghini, "
                      "but is clearly different from the brands current line of super sports cars."),
                     thumbnail_picture="../../static/images/models/lamborghini-asterion-thumbnail.jpg",
                     auto_maker=auto_maker3)

session.add(auto_model12)
session.commit()

auto_model_image45 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-asterion-1.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model12)

auto_model_image46 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-asterion-2.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model12)

auto_model_image47 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-asterion-3.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model12)

auto_model_image48 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/lamborghini-asterion-4.jpg",
                                   auto_maker=auto_maker3,
                                   auto_model=auto_model12)

session.add_all([auto_model_image45, auto_model_image46, auto_model_image47, auto_model_image48])
session.commit()



# Catalog for Ferrari
auto_maker4 = AutoMaker(user_id=1, name="Ferrari",
                        description=("Born in 1947, Ferrari has always produced vehicles at its "
                          "current site and has maintained its directions. It has progressively "
                          "widened its range using visionary planning both on a design level "
                          "and on the quality of work produced."),
                        thumbnail_picture="../../static/images/models/ferrari-thumbnail.jpg",
                        banner_picture="../../static/images/models/ferrari-banner.jpg")

session.add(auto_maker4)
session.commit()

auto_model13 = AutoModel(user_id=1, name="488 Spider",
                     description=("The Ferrari 488 Spider is the latest chapter in Maranellos "
                      "ongoing history of open-top V8 sports cars, a story that started with "
                      "the targa-top version of the 308 GTB  - the immortal 308 GTS - and "
                      "which ultimately resulted in the full convertible Spider architecture. "),
                     thumbnail_picture="../../static/images/models/ferrari-spider-thumbnail.jpg",
                     auto_maker=auto_maker4)

session.add(auto_model13)
session.commit()

auto_model_image49 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-spider-1.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model13)

auto_model_image50 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-spider-2.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model13)

auto_model_image51 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-spider-3.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model13)

auto_model_image52 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-spider-4.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model13)

session.add_all([auto_model_image49, auto_model_image50, auto_model_image51, auto_model_image52])
session.commit()

auto_model14 = AutoModel(user_id=1, name="488 GTB",
                     description=("The 488 GTB name marks a return to the classic Ferrari model "
                      "designation with the 488 in its moniker indicating the engines unitary "
                      "displacement, while the GTB stands for Gran Turismo Berlinetta. "
                      "The new car not only delivers unparalleled performance, it also makes "
                      "that extreme power exploitable and controllable to an unprecedented "
                      "level even by less expert drivers."),
                     thumbnail_picture="../../static/images/models/ferrari-gtb-thumbnail.jpg",
                     auto_maker=auto_maker4)

session.add(auto_model14)
session.commit()

auto_model_image53 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-gtb-1.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model14)

auto_model_image54 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-gtb-2.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model14)

auto_model_image55 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-gtb-3.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model14)

auto_model_image56 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-gtb-4.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model14)

session.add_all([auto_model_image53, auto_model_image54, auto_model_image55, auto_model_image56])
session.commit()

auto_model15 = AutoModel(user_id=1, name="458 Speciale",
                     description=("As the most extremely-focused Ferrari V8 sports car in history, "
                      "the 458 Speciale bristles with technical solutions that make it unique for "
                      "owners seeking an even more extreme sports car. Innovations span the entire "
                      "car, including Ferrari patents and world firsts."),
                     thumbnail_picture="../../static/images/models/ferrari-speciale-thumbnail.jpg",
                     auto_maker=auto_maker4)

session.add(auto_model15)
session.commit()

auto_model_image57 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-speciale-1.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model15)

auto_model_image58 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-speciale-2.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model15)

auto_model_image59 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-speciale-3.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model15)

auto_model_image60 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-speciale-4.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model15)

session.add_all([auto_model_image57, auto_model_image58, auto_model_image59, auto_model_image60])
session.commit()

auto_model16 = AutoModel(user_id=1, name="LaFerrari",
                     description=("The LaFerrari needs few superlatives. It is our most ambitious "
                      "project yet, pushing the boundaries of technology for a road car. It gathers "
                      "together the marques greatest technical capabilities from both GT and "
                      "Formula 1 engineering, delivering the highest performance ever reached by a "
                      "production Ferrari. "),
                     thumbnail_picture="../../static/images/models/ferrari-laferrari-thumbnail.jpg",
                     auto_maker=auto_maker4)

session.add(auto_model16)
session.commit()

auto_model_image61 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-laferrari-1.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model16)

auto_model_image62 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-laferrari-2.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model16)

auto_model_image63 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-laferrari-3.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model16)

auto_model_image64 = AutoModelImage(user_id=1,
                                   image_url="../../static/images/models/ferrari-laferrari-4.jpg",
                                   auto_maker=auto_maker4,
                                   auto_model=auto_model16)

session.add_all([auto_model_image61, auto_model_image62, auto_model_image63, auto_model_image64])
session.commit()


print "Added catalog items!"
