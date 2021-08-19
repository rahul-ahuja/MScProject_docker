# Instructions to run the application

### Option 1: Running the application locally

#### pull postgres docker image from public repo

docker run --name {docker_container_name} -p 5432:5432 -e POSTGRES_USER={POSTGRES_USER} -e POSTGRES_PASSWORD={POSTGRES_PASSWORD} -d postgres

#### create a role with the below command;

python roles_setup.py

#### create database tables

python models.py

#### run the flask app

python main.py


### Option 2: run the application through docker compose where the docker images will be downloaded from the dockerhub repository;

docker-compose up --scale webapp={number of container replicas}


# Guide to what files are being submitted;

1. main.py contains all the application backend logic
2. models.py contains the creation of the database tables
3. roles_setup.py contains the code for creating access based role for the developer
4. geocode.py contains external rest api implementation to call the google api to get the location coordinates 
5. restuarant.py contains external rest api implementation to call the foursquare api to get the restuarant names according to the location co-ordinates.
6. psql_exp.py contains the code to show that the developer has certain priviledges
7. test_flaskr.py contains the application testing codes
8. requirements.txt file contains all the python dependences needed to be installed to run the application
9. Dockerfile contains the script to create the docker image of the application
10. docker-compose.yml contains the script to configure nginx, postgres docker image and application docker image as a single network
11. app.log contains the logs of the HTTP responses codes and header content
12. templates folder contains the HTML pages;
	a. base.html, index.html and layout.html files are the basic layouts of the application interface
	b. login.html is the display of login endpoint
	c. proposals.html is the display of the proposals endpoint
	d. register.html is the display of the register endpoint
	e. requests.html is the display of the requests endpoint
	f. welcome.html is the display of the entry point of the application API
13. static folder contains the CSS and JavaScript files to sylized the content of the HTML files.
