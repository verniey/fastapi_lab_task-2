#  Restaurant Menu System Assignment

Write tests for the API endpoints.

Wrap your software components in containers. The containers should be started with a single command "docker-compose up -d" or the one you specify in the README.md.

Docker Images:
(API) python:3.10-slim
(DB) postgres:15.1-alpine

1. Write CRUD tests for the previously developed API using the pytest library.
2. Prepare a separate container to run the tests. Specify the command to run in the README.md.
3. * Implement retrieving the count of submenus and dishes for a Menu using a single (complex) ORM query.
4. ** Implement the test scenario "Check the count of dishes and submenus in a menu" from Postman using pytest. 

If FastAPI is synchronous, the tests are synchronous. If it's asynchronous, the tests are asynchronous.


## Running the Application

To run the application and the database in containers, follow these steps:

1. Install Docker and Docker Compose on your system.
2. Clone this repository: `git clone https://github.com/verniey/fastapi_lab_task-2`
3. Navigate to the project directory: `cd your-fastapi-app`
4. Create a .env file in the project root directory and add the required environment variables. Here's an example of .env file:
```env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
SECRET_KEY=mysecretkey
```
5. Create vertual enviroment `python -m venv venv`  and activate a virtual environment `source venv/bin/activate`(recommended). To deactivate `deactivate`
6. Modify the configuration settings in `docker-compose.yml` as needed.

## Running Tests

Build the Image: Make sure you have built the Docker image for the app service using the correct Dockerfile. Run the command `docker-compose build app` to build the image.

To run the tests, make sure the containers are running using the `docker-compose up -d` command, and then run:

```bash
docker-compose exec app pytest
```
Or run `docker-compose up --build -d`, it combines the build and run commands into a single step. 

To stop and remove the containers, run:
`docker-compose down`
