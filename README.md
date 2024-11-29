# QuizlyTime - Online Quiz App
## How to setup with Docker
1. Pull the main branch
2. create a .env file in the root directory of the project and do the following:
    - create a DB_URI env variable with a URI to your mongodb collection
    - create a JWT_SECRET env variable with a string. This will be used to generate JWTs so create a secure secret (You could use a uuid creation library).
3. Download and open Docker Desktop, if you don't already have it.
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
![uml](https://github.com/user-attachments/assets/c555ad1f-d6ef-4581-80d8-5bddc960127d)

## MVC Architecture
- Models (./models):
    - User model: Schema for how user documents are structured.
    - Question model: Schema for how quiz question documents are structured.
    - Quiz model: Schema for how quiz documents are structured.
- Views (./views/pages):
    - Home: default landing page for the app.   
    - Login: handles login inputs and sends requests to user_controller.py endpoints.
    - Register: handles registration inputs and sends requests to user_controller.py endpoints.
    - Profile: displays user game history, created quizzes and statistics. Sends requests to user_controller.py endpoints.
    - ChooseQuizType: page to choose to play either randomly created quizzes or user create quizzes.
    - Random Quiz Pages:
        - QuizSetup: handles settings selection for playing random quiz. Sends requests to quiz_controller.py
        - Quiz: handles the quiz gameplay using sockets. Game is handles via sockets. Socket endpoints in quiz_controller.py
        - QuizComplete: displays end of game score.
    - User-created Quiz Pages:
        - CreateQuizSetup: handles input for quiz settings (title and # of questions).
        - CreateQuiz: handles input for question creation. Sends requests to custom_quiz_controller.py
        - CreateQuizComplete: Page shown on successful custom quiz creation.
        - QuizSelection: displays all user created quizzes avaliable to play. Sends requests to custom_quiz_controller.py and quiz_controller.py
- Controllers (./controllers):
    - user_controller: handles requests regarding account creation, authetication and user statistics.
    - quiz_controller: handles requests regarding random quiz creation and quiz gameplay loop via sockets.
    - custom_quiz_controller: handles requests regarding user-created quiz creation, retrieval, editting and deletion.
- Services (./services):
    - auth_service: responsible for creating and validating jwts and passwords.
    - quiz_service: responsible for mapping retrieved questions from api into questions stored in our db.
  
