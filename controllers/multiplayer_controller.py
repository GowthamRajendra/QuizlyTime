from flask_socketio import Namespace, emit, join_room, leave_room
from flask import jsonify, make_response, request
import random
import string
import requests
from models.quiz_model import Quiz, AnsweredQuestion
from models.user_model import User
from models.question_model import Question
from services.quiz_service import store_questions, create_quiz_questions
from datetime import datetime 
from time import sleep
from threading import Thread

'''
TODO:
CURRENT: on_check_answer logic
- Game settings
- Gameplay loop
  - Question retrieval and distribution
  - Syncing timers
  - Incrementing questions for all players at the same time
  - Player results leaderboard
- Wayyy later, redis + multiple docker backend + load balancer
'''
rooms = {
    # roomCode: {players:{sid1: {player state}, ...}, status:"waiting, started or ended"}
}
sid_to_player = {
    # request.sid: {name, email, etc.}
}
sid_to_room = {
    # request.sid: roomcode
}

def generateRoomCode(length=6):
    room = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # don't want dupes, even though very very rare.
    while room in rooms:
        room = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    return room

def getNamesInRoom(room):
    players = rooms[room]['players']
    names = []
    for sid in players:
        names.append(sid_to_player[sid]['name'])
    
    return names

def getEmailsInRoom(room):
    players = rooms[room]['players']
    names = []
    for sid in players:
        names.append(sid_to_player[sid]['email'])
    
    return names

# check if everyone in a room has answered the current questions
def getAnsweredInRoom(room):
    players = rooms[room]['players']
    print("CHECKING IF EVERYONE ANSWERED: ", players)
    # print(players.values())
    check = all([player['answered'] for player in players.values()])
    
    return check

# get scores, format em, sort em and return em for the results screen post-game
def getScoresInRoom(room):
    players = rooms[room]['players']

    scores = []

    for sid, game_state in players.items():
        scores.append({'name': sid_to_player[sid]['name'], 'score': game_state['score']})
    
    # sort by score, descending
    scores.sort(key=lambda x: x['score'], reverse=True)

    print(scores)

    return scores

category_dict = {
    '': 'Any Category',
    '9': "General Knowledge",
    '10': "Entertainment: Books",
    '11': "Entertainment: Film",
    '12': "Entertainment: Music",
    '13': "Entertainment: Musicals & Theatres",
    '14': "Entertainment: Television",
    '15': "Entertainment: Video Games",
    '16': "Entertainment: Board Games",
    '17': "Science & Nature",
    '18': "Science: Computers",
    '19': "Science: Mathematics",
    '20': "Mythology",
    '21': "Sports",
    '22': "Geography",
    '23': "History",
    '24': "Politics",
    '25': "Art",
    '26': "Celebrities",
    '27': "Animals",
    '28': "Vehicles",
    '29': "Entertainment: Comics",
    '30': "Science: Gadgets",
    '31': "Entertainment: Japanese Anime & Manga",
    '32': "Entertainment: Cartoon & Animations"
}

class MultiplayerNamespace(Namespace):
    def on_connect(self):
        print('multiplayer connection established')
        print(request.sid)

    # clean up dictionary entries on disconnection of any kind.
    def on_disconnect(self):
        name = sid_to_player.get(request.sid, {}).get('name')
        room = sid_to_room.get(request.sid)

        if room and room in rooms:
            leave_room(room)
            rooms[room]['playerCount'] -= 1

            self.emit('player_left', {'name': name}, room=room)

            # remove player from room player game state
            rooms[room]['players'].pop(request.sid, None)

            # if no more players, delete room from dictionary
            if rooms[room]['playerCount'] <= 0:
                print("DELETING ROOM, NO MORE PLAYERS")
                rooms.pop(room, None)

        # cleanup disconnected players entries in sid dictionaries
        sid_to_player.pop(request.sid, None)
        sid_to_room.pop(request.sid, None)

        # TODO NEED TO HANDLE PLAYERS LEAVING DURING THE MATCH
        # CHECK IF AFTER SOMEONE LEAVES, EVERYONE LEFT HAS ALREADY ANSWERED

    # storing user information after successful connection.
    # client side only needs to send info once, convinient to get info
    # with request sid.
    def on_register_user(self, data):
        # no need to store the same info again
        if request.sid in sid_to_player:
            return

        email = data.get('email')
        name = data.get('name')

        if not email or not name:
            return # error
        
        sid_to_player[request.sid] = {"email": email, "name": name}

        print('User registered', request.sid, sid_to_player[request.sid])

    # generate room and create a multiplayer room.
    def on_create_room(self):
        # if user info wasn't successfully registered.
        if request.sid not in sid_to_player:
            return

        # prevent player from creating multiple rooms
        if request.sid in sid_to_room:
            return
        
        room = generateRoomCode()
        print(room)

        # join socket room, add room to dict with initial game state.
        join_room(room)
        rooms[room] = {'players': {request.sid: {'score': 0, 'active': True, 'answered': False, 'answer': '', 'correct': False}}, 'questionIndex': 0 , 'playerCount': 1, 'status': 'waiting'}
        
        # easy to get what room a socket is in.
        sid_to_room[request.sid] = room

        # send initial update to the lobby creator
        self.emit('room_created', {'code': room}, room=room)
        self.emit('player_joined', {'names': getNamesInRoom(room)}, room=room)
    
    def on_join_room(self, data):
        # if player info was not successfully recorded
        if request.sid not in sid_to_player:
            return

        # prevent player from joining multiple rooms
        if request.sid in sid_to_room:
            return
        
        room = data.get('code')

        if room not in rooms:
            return # error room doesnt exist
        
        # add new player game state to room and update room entry and sid_to_room dict
        new_player = {'score': 0, 'active': True, 'answered': False}
        
        join_room(room)
        rooms[room]['players'][request.sid] = new_player
        rooms[room]['playerCount'] += 1
        sid_to_room[request.sid] = room

        print(f"players in room {room}", rooms[room]['players'])

        # send room code and list of all players to display on client sides
        self.emit('room_created', {'code': room}, room=room)
        self.emit('player_joined', {'names': getNamesInRoom(room)}, room=room)
    
    def on_current_players(self):
        if request.sid not in sid_to_room:
            return
        
        room = sid_to_room[request.sid]

        # reusing the player_joined endpoint because all the times we return name
        # is just for updating client side player list.
        self.emit('player_joined', {'names': getNamesInRoom(room)}, room=room)
    
    def on_start_game(self, data):
        if request.sid not in sid_to_room:
            return
        
        room = sid_to_room[request.sid]

        amount = data.get('amount')
        type = data.get('type')
        difficulty = data.get('difficulty')
        category = data.get('category')

        API_URL = f'https://opentdb.com/api.php?amount={amount}&type={type}&difficulty={difficulty}&category={category}'

        response = requests.get(API_URL).json()

        print(response)

        # store the questions in the database, and return the question objects as a list
        questions = store_questions(response['results'])
        
        # create a new quiz object and store it in the database
        # set timestamp to the current time since the quiz is just starting
        quiz = Quiz(title=category_dict[category], score=0, timestamp=datetime.now(), total_questions=amount, questions=questions)
        quiz.save()

        # set all the user's active quiz to this one.
        emails = getEmailsInRoom(room)

        for email in emails:
            user = User.objects(email=email).first()
            print(user.email, user.username)
            user.active_quiz = quiz
            user.save()

        quiz_questions = create_quiz_questions(questions)

        print(quiz_questions)
        
        self.emit('start_game', {'questions': quiz_questions}, room=room)
    
    def on_check_answer(self, data):
        if request.sid not in sid_to_player:
            print("player information not registered")
            return
        
        email = sid_to_player[request.sid]['email']
        user = User.objects(email=email).first()
        quiz = user.active_quiz
        question_index = data['question_index']

        # dont check the answer if the user doesn't have an active quiz
        if quiz is None:
            print("no active quiz")
            return
        
        # players needs to be in a room
        if request.sid not in sid_to_room:  
            return
        
        # UPDATE PLAYER GAME STATE
        room = sid_to_room[request.sid]
        player_game_state = rooms[room]['players'][request.sid]
        player_game_state['answered'] = True
        player_game_state['answer'] = data['user_answer']

        # get the question object from the question id
        question = Question.objects(pk=data['question_id']).first()
        print(question.category)

        # check if the answer is correct
        if data['user_answer'] == question.correct_answer:
            print(question.correct_answer)
            player_game_state['correct'] = True
            
            # scale points to time left
            if data["time_left"] / data["max_time"] > 0.75:
                player_game_state['score'] += 10
            else:
                player_game_state['score'] += 10 * (data["time_left"] / data["max_time"])
        else:
            player_game_state['correct'] = False

        # print("results", results)
        # wait until everyone has answered to return results.
        if not getAnsweredInRoom(room):
            print("WAITING FOR MORE PLAYERS TO ANSWER")
            return 

        print("EVERYONE ANSWERED, CHECKING AND SENDING RESULTS")

        # store the question and user's answer in the answered_questions list
        # NEED TO CHANGE THIS LOGIC, KEPT FOR TESTING
        quiz.answered_questions.append(
            AnsweredQuestion(question=question, user_answer=data['user_answer'])
        )

        quiz.save() 

        answers = []

        # get names, answers and whether they were correct
        for sid, data in rooms[room]['players'].items():
            username = sid_to_player[sid]['name']
            answers.append({
                "username": username,
                "user_answer": data['answer'],
                "is_correct": data['correct']
            })

            data['answered'] = False
        
        # send everyones results to everyone
        results = {
            "correct_answer": question.correct_answer,
            "question_index": question_index,
            "answers": answers
        }

        print("EVERYONES RESULTS: ", results)
        # Need to emit list of player resuls to everyone.
        self.emit('answer_checked', results, room=room)

        Thread(target=self.sleepThenContinueQuiz, kwargs={"user": user, "quiz": quiz, "room": room}).start()

    def on_leave_room(self):
        name = sid_to_player.get(request.sid, {}).get('name')
        room = sid_to_room.get(request.sid)

        if room and room in rooms:
            leave_room(room)
            rooms[room]['playerCount'] -= 1

            self.emit('player_left', {'name': name}, room=room)

            # remove player from room player game state
            rooms[room]['players'].pop(request.sid, None)

            # if no more players, delete room from dictionary
            if rooms[room]['playerCount'] <= 0:
                print("DELETING ROOM, NO MORE PLAYERS")
                rooms.pop(room, None)
        
        sid_to_room.pop(request.sid, None)
        self.emit('leave_room_successful', room=request.sid)
    
    # chat for testing room functionality. may because a feature later
    def on_player_message(self, data):
        message = data.get("message")

        # dont send empty messages
        if not message:
            return # error
        
        # dont send messages if user is not in a room
        if request.sid not in sid_to_room:
            return
        
        name = sid_to_player[request.sid]['name']
        room = sid_to_room[request.sid]

        self.emit('player_message', {"message" : message, "name": name}, room=room)

    # HELPER FUNCTIONS
    # buffer between sending question results and moving to next question
    # so clients have time to see results
    def sleepThenContinueQuiz(self, user: User, quiz: Quiz, room: str, seconds: int=2):
        sleep(seconds)

        if len(quiz.answered_questions) != quiz.total_questions:
            print('NEXT QUESTION')
            rooms[room]['questionIndex'] += 1
            self.emit('next_question', {"newQuestionIndex": rooms[room]['questionIndex']})
            return

        # Quiz completed, store results.
        
        self.emit('quiz_completed', {"scores": getScoresInRoom(room)}, room=room)

        # TODO: storing results, commented out is the singleplayer version
        # problem with current approach is that only the last user to answer has their
        # AnsweredQuestion saved to the Quiz document. Need to figure out a way to store
        # everyone's results. Also need to discard users who dont actually finish the quiz?
        # if quiz.user_created:
        #     # create copy of quiz for user
        #     quiz_history = Quiz(
        #         title=quiz.title, 
        #         score=quiz.score, 
        #         timestamp=datetime.now(), 
        #         total_questions=quiz.total_questions, 
        #         questions=quiz.questions,
        #         answered_questions=quiz.answered_questions
        #     )
        #     quiz_history.save()
        #     user.completed_quizzes.append(quiz_history)
        
        #     # reset original quiz
        #     quiz.answered_questions = []
        #     quiz.score = 0
        #     quiz.save()

        # # else its an randomly created quiz and just append it
        # else:
        #     user.completed_quizzes.append(quiz)

        # user.active_quiz = None
        # user.save()


        

