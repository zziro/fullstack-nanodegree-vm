# Sport Catalog Project

The next project will show you a list of product's categories related to a sport that you like.
You will be able to ADD, READ, UPDATE and DELETE differents categories and its subcategories and details.

## Getting started

### Prerequisites
The run this project you will need install some tools such as:

* Install Virtual Box: For this project we will use Virtual Box 5.1.34. It can be downloaded [here].<br />

[here]:https://www.virtualbox.org/wiki/Download_Old_Builds_5_0

* Install Vagrant: 	
	* Fork the repo and clone the project.<br />
		git clone https://github.com/{username}/fullstack-nanodegree-vm/tree/master/vagrant/catalog catalog_project
	* This will generate a catalog_project folder.
	* Change directory to vagrant folder.
	* Inside vagrant folder, run the following command in order to run the virtual machine.<br />
		vagrant up
	* Once the virtual machine is up, run the following command to login: <br />
		vagrant ssh

* Generating Credentials <br />
The Sport Catalog project has the alternative to login with your Google+ account, using OAuth 2.0. To do that, you need to generate and secret key.
	* Go to the [Google Developer Console].
	* Create New Project.
	* Enable the Google+ API.
	* On the left menu, click on Credentials.	
	* Select Create Credential. From the dropdown choose OAuth client ID.
	* Make sure the option 'Authorised JavaScript origins', is filled like URL. (http://localhost:5000)
	* Once you will have finished,  download the JSON file and rename it as: client_secrets.json and paste it inside the catalog_project folder.


[Google Developer Console]:https://console.cloud.google.com
### Running the project

* Inside the catalog_project, run the following commands:
	* To configure the database: python database_setup.py
	* To load data: python database_data.py
	* To run the app: python application.py

After that, open your browser and type: http://localhost:5000.

### Endpoints

The catalog project exposes JSON, which can be consumed for whatever application. 

* Enpoint showing all sport categories
	http://localhost:5000/category/JSON

*  Catalog's categories with its items
	http://localhost:5000/category/1/item/JSON
