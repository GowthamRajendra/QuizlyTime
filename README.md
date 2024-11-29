# QuizlyTime - Online Quiz App
## How to setup
1. Pull the main branch
2. create a .env file in the root directory and do the following:
  - create a DB_URI env variable with a URI to your mongodb collection
  - create a JWT_SECRET env variable with a string. This will be used to generate JWTs so create a secure secret (You could use a uuid creation library).
3. Download Docker Desktop, if you don't already have it.
4. In your terminal of choice while in the root directory of the project run the following commands:
  - docker-compose build
  - docker-compose up
5. The frontend and backend should be up and running. The frontend will be accessible on http://localhost:5173

## UML Diagram
- picture
