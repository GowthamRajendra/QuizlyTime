import os

# only patch in production, pytests wont work when patched
# patching standard lib required for gevent and redis to work properly.
if os.environ.get('FLASK_ENV') == 'production':
    import eventlet
    eventlet.monkey_patch()

# load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv(override=True)

from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from socket_manager import socketio
from controllers.quiz_controller import SinglePlayerNamespace
from controllers.multiplayer_controller import MultiplayerNamespace
from sys import argv

def create_app():
    app = Flask(__name__)

    # set up config
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
    app.config['MONGO_URI'] = os.getenv('DB_URI')

    # import blueprints
    from controllers.user_controller import users_bp    
    from controllers.quiz_controller import quiz_bp
    from controllers.custom_quiz_controller import custom_quiz_bp

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(custom_quiz_bp)

    # connect to the database
    connect('QuizAppDB', host=app.config['MONGO_URI'], uuidRepresentation="standard")

    # initialize socketio
    # change cors_allowed_origins later
    socketio.init_app(app, cors_allowed_origins=os.getenv('FRONT_END_URL','*'))

    # register singleplayer and multiplayer namespaces
    socketio.on_namespace(SinglePlayerNamespace('/singleplayer'))
    socketio.on_namespace(MultiplayerNamespace('/multiplayer'))

    # @socketio.on('check_answer')
    # def test(data):
    #     print('checking answer')
    #     print(data)
    #     emit('answer_checked', data, broadcast=True)

    return app

app = create_app()
CORS(
    app, 
    supports_credentials=True,
    origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"]
)

if __name__ == '__main__':
    if len(argv) > 1:
        port = argv[1]
    else:
        port = os.getenv('PORT', 5000)

    socketio.run(app, host="0.0.0.0", port=int(port) , debug=os.getenv('FLASK_ENV', True))
