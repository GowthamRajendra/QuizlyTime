import os
from dotenv import load_dotenv
load_dotenv(override=True)

# only patch in production, pytests wont work when patched
# patching standard lib required for eventlet and redis to work properly.
if os.getenv("TESTING") == None:
    import eventlet
    eventlet.monkey_patch()

import boto3

# load envs from parameter store if this is an ec2
if (os.getenv("AWS_ENV") == "true"):
    ssm = boto3.client('ssm', region_name='us-east-2')
    response = ssm.get_parameters_by_path(
        Path="/quizapp/",
        WithDecryption=True
    )
    
    for param in response['Parameters']:
        key = param['Name'].split('/')[-1]
        os.environ[key] = param['Value']

# initialize redis after envs are loaded
from redis_client import init_redis
init_redis()

from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from socket_manager import socketio
from controllers.quiz_controller import SinglePlayerNamespace
from controllers.multiplayer_controller import MultiplayerNamespace

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
    app.config['MONGO_URI'] = os.getenv('DB_URI')

    from controllers.user_controller import users_bp    
    from controllers.quiz_controller import quiz_bp
    from controllers.custom_quiz_controller import custom_quiz_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(custom_quiz_bp)

    connect('QuizAppDB', host=app.config['MONGO_URI'], uuidRepresentation="standard")

    if os.getenv("TESTING"):
        socketio.init_app(app, async_mode="eventlet", cors_allowed_origins=os.getenv('FRONT_END_URL','*'))
    else:
        socketio.init_app(
            app, 
            async_mode="eventlet",
            message_queue=f'{os.getenv("REDIS_URL", "redis://localhost:6379")}/0',
            cors_allowed_origins=os.getenv('FRONT_END_URL','*')
            )

    # register namespaces
    socketio.on_namespace(SinglePlayerNamespace('/singleplayer'))
    socketio.on_namespace(MultiplayerNamespace('/multiplayer'))

    return app

app = create_app()
CORS(app, 
     supports_credentials=True,
     origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"]
)

if __name__ == '__main__':
    socketio.run(app, 
                 host="0.0.0.0", 
                 port=int(os.getenv('PORT', 5000)), 
                 debug=os.getenv('FLASK_ENV', True) == "prod")
