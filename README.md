# Option 1

#### Run locally

##### pull postgres docker image from public repo

docker run --name {docker_container_name} -p 5432:5432 -e POSTGRES_USER={POSTGRES_USER} -e
POSTGRES_PASSWORD={POSTGRES_PASSWORD} -d postgres

##### after cloning this repo, create a role
python roles_setup.py

##### create database tables 
python models.py

##### run the flask app
python main.py


# Option 2

##### run the application through docker compose
docker-compose up --scale webapp={number of container replicas}
