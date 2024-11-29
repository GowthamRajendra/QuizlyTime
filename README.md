# QuizlyTime - Online Quiz App
## How to setup with Docker
1. Pull the main branch
2. create a .env file in the root directory of the project and do the following:
    - create a DB_URI env variable with a URI to your mongodb collection
    - create a JWT_SECRET env variable with a string. This will be used to generate JWTs so create a secure secret (You could use a uuid creation library).
3. Download Docker Desktop, if you don't already have it.
4. In your terminal of choice while in the root directory of the project run the following commands:
    - docker-compose build
    - docker-compose up
5. The frontend and backend should be up and running. The frontend will be accessible on http://localhost:5173

## How to setup without Docker
1. Pull the main branch
2. create a .env file in the root directory of the project and do the following:
    - create a DB_URI env variable with a URI to your mongodb collection
    - create a JWT_SECRET env variable with a string. This will be used to generate JWTs so create a secure secret (You could use a uuid creation library).
3. cd into the root directory of the project
4. Create a python virtual environment in the root directory of the project by running the following:
    - python -m venv .venv
5. Activate the venv
    - (On windows): .venv\Scripts\Activate
6. pip install -r requirements.txt
7. cd views
8. npm i (You will need to install node.js to do this if you don't already have it)
9. npm run dev
10. Open a second terminal
11. cd into the root directory of the project (where app.py is)
12. python app.py
13. Both the frontend and backend should now be running. The frontend will be accessible on http://localhost:5173

## UML Diagram
- picture
