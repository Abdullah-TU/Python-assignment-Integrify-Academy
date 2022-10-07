# Python assignment: Integrify Academy
## Md. Abdullah-Al Mamun

## Basic requirements:
● Language: Python
● Framework: Flask
● Database: PostgreSQL

## The basic functionality of each file in the app:
#### Constants.py
##### This file will contain the constant if you see the document there is a path given the name api-v1 so for good practice we have separated it. 

#### authController.py
#####  authController.py file for the auth controller. All the work that is related to logging in, registering, and register and change passwords is working here.

#### todoController.py
##### This file is responsible for the todos list api. To add the item to the to-do list, to get the to-do list, or to delete or update the list, and so on.

#### ServerResponse.py
##### All responses which will be sent to the user will map by this method the main purpose to use this is to ensure the whole api response will be one.

#### Models.py
##### Models.py file is responsible to do database-related work to get data from the database, save data in the database, make the table in the database, and many more. while things are happening here.
#### App.py
##### We are starting from this file. This is the main file which is the entry point of the flask from this file. This is basically setting up the configuration of the flask and telling the flask these must be the routes and actions of the todos api and setting up the database keys and so on.

#### Readme.md
##### Details Information about the app.
##### How to run it?
#### Requirements.txt
##### Requirements.txt is a text file. It shows all the requirements for this app.


## How to run the API on our local environment?
##### First install all packages require using command: 
```
pip install -r requirements.txt
```
##### Then, update your db url in .env file 
##### After installing above requirement and changing env, the next step will be to run the flask.

```
flask run -p 8200
```

##### Above command -p defines the port number you can change according to your needs. for example, currently the server is running on 8200 port.

##### The postman collection is also attached in the project. We should import it in our postman.

###### Following is the url of api documentation:

https://documenter.getpostman.com/view/9134823/2s83zcTSu9

## How to run this project? : (briefly in the video)

https://user-images.githubusercontent.com/16822543/194448048-e57b102c-000b-41e9-8ebb-fea3d9d181b7.mp4




