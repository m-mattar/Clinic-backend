# CSE Clinic

## About
The project consists of an application front for a Mental Care system. 
Its purpose is to facilitate Patients Appointment taking and Monitoring, especially during the COVID-19 crisis.

All users are registered by the Admin and given their credentials.
Patients are able to search for doctors, take a look at their upcoming appointments and reports, and attend consultations via an automatically generated zoom link.
Doctors are able to see all their patient's reports in order to monitor their case. They are also required to write new reports after every consultation.

## Technologies
This repository consists of the application Backend. 
It involves a REST Flask API and was built using Python and a mysql database. 

## Setup

### Step 1 : Install Flask
Using the command prompt, Enter : pip install Flask
You could also create a virtual environment and install Flask within it, if so, all the below steps must be done in the environment.

### Step 2 : Clone the repository
In order to clone the backend repository :
Create a new folder, anywhere in your PC
Open Command Prompt and change the directory into the folder created
Enter : git clone https://github.com/m-mattar/430-project-backend

### Step 3 : Install Packages
All the direct and transitive dependencies are available in the requirements.txt file

Using the Command Prompt, Enter : pip install -r requirements.txt
Make sure that the Command Prompt is pointing to the "430-project-backend" folder

### Step 4 : Initialize the local database
To make things simple, all database models are available in the initializer.py file

First, you need to create a new mysql schema, call it "hospital".
In the app/__init__.py file, you can find the link to your local database at line 16, please put your password in place of "password"

Using the Command Prompt, Enter : python
This will open a python shell
Enter the below commands:
from initializer import db
db.create_all()
exit()

You have successfully initialized your database!

### Step 5 : Run the Backend
In order to run the Backend, you need to enter the following commands in your Command Prompt:
set FLASK_APP=server.py
flask run

Your backend is now running on port 5000!

### Step 6 : Run the Frontend
Please see the Backend's Repo for more details on how to run the application's frontend. You can find the link below!
The frontend can be found here: https://github.com/HusseinJaber20/Clinic---430

### Note : creating the admin account
The admin has absolute priviledges on the Application, hence creating it requires direct backend or database access.

- Option 1 : Manually add the admin user from the database
- Option 2 : 
  * Go to the api/User.py file
  * Comment out line 24 and 25 ( "if not is_admin_login(request)" condition )
  * Run the Backend
  * Create the admin user from the fronted. Note that it is required that the username used for the admin is "admin"
  * Uncomment the previously commented lines
  * Run your backend again

Everything is now perfectly set up!

Enjoy our application! :)










