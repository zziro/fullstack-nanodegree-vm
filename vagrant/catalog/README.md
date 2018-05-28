# Sport Catalog Project

The next project will show you a list of product's categories related to a sport that you like.
You will be able to ADD, READ, UPDATE and DELETE the differents categories and its subcategories and details.

## Getting started

### Prerequisites
The run this project you will need install some tools such as:

* Install Virtual Box: For this project we will use Virtual Box 5.1.34. It can be downloaded [here].<br />

* Install Vagrant: 
	* It can download it from this [repo]. It normally takes place at the Downloads folder.
	* Fork the repo and clone the project.<br />
		git clone https://github.com/{username}/fullstack-nanodegree-vm/tree/master/vagrant/catalog catalog_project
	* Change directory to vagrant folder.
	* Inside vagrant folder, run the following command in order to run the virtual machine.<br />
		vagrant up
	* Once the virtual machine is ip, run the following command to login: <br />
		vagrant ssh

[repo]:https://github.com/udacity/fullstack-nanodegree-vm
[here]:https://www.virtualbox.org/wiki/Download_Old_Builds_5_0

* Generating Credentials
The Catalog project has the alternative to login with your Google+ account, ussing OAuth 2.0. To do that, you need to generate and secret key.
	* Go to the [Google Developer Console].
	* Create New Project.
	* Enable the Google+ API.
	* On the left menu, click on Credentials.	
	* Select Create Credential. From the dropdown choose OAuth client ID.
	* Make sure the option 'Authorised JavaScript origins', is filled like a URL. (http://localhost:5000)
	* Once you will have finished,  download the JSON file and reanem it as : client_secrets.json and paste it inside the catalog_project folder.


[Google Developer Console]:https://console.cloud.google.com
### Running te project

* Inside the catalog_project, run the following commands:
	* To configure the database: python database_setup.py
	* To load data: python database_data.py
	* To run the app: python application.py

After that, open your browser and type: http://localhost:5000.
