# luxury-rides-catalog
This project is a Python-based responsive web application built on the flask framework, that provides a list of luxury cars within a variety of auto makers.
It also provides a user registration/authentication and authorization system through Google+. Logged in users have the ability to 
post, edit and delete their own items. The application also provides JSON and XML API endpoints for querying its data.

### Requirements ###
1. Python 2.7 or above should be installed on your computer. Instructions for checking if python is installed, or for downloading and installing it, can be found here: https://wiki.python.org/moin/BeginnersGuide/Download
2. Vagrant Virtual machine and VirtualBox. The Vagrant VM has already been installed and configured on the repo you'll download, so you do not need to worry about that. For Virtual Box, instructions for downloading and installing it for your OS can be found here: https://www.virtualbox.org/wiki/Downloads

### Getting Started ###
1. Download the repo as a zip file to your computer (luxury-rides-catalog-master.zip)
2. Unzip the downloaded file, save the extracted folder to a location of your choice
3. To use the Vagrant VM, launch terminal on MAC or the Command prompt on Windows, and navigate to where you stored the unzipped folder, and into luxury-rides-catalog-master
4. Power on the virtual machine by typing the command vagrant up
5. Then log into the virtual machine by typing the command vagrant ssh
6. Change directory to the synced folders by typing the command cd /vagrant
7. Start the web application by typing the command python application.py
8. Navigate to the link http://localhost:5000/catalog on any browser of your choice to see and explore the catalog
