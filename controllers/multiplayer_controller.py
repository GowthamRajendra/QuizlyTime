from flask_socketio import Namespace, emit, join_room, leave_room
from flask import request
import random
import string
import requests
from models.quiz_model import AnsweredQuestion
from models.multiplayer_quiz_model import MultiplayerQuiz, MultiplayerParticipant
from models.user_model import User
from models.question_model import Question
from services.quiz_service import store_questions, create_quiz_questions
from datetime import datetime 
from time import sleep
from threading import Thread
from services.multiplayer_service import *

'''
TODO:
- Redis
    - REPLACE IN-MEMORY DICT AND ALL RELATED FUNCTIONS AND USAGE WITH REDIS
- Load balancer + multiple containers
'''

# rooms -> redis hashmap key is room:code, value is current room state without the players field
# players -> redis hashmaps key is room:code:player:sid, value is player game state
# each player is now a seperate hashmap because we need to frequently update the fields
# rooms = {
#     # roomCode: {players:{sid1: {player state}, ...}, status:"waiting, started or ended"}
# }

# sid_to_player -> redis hashmap same thing, key is sid, value is {name, email, etc.}
# nested hashmaps are fine here because we won't be updating as fields, just inserting and deleting entries.
# sid_to_player = {
#     # request.sid: {name, email, etc.}
# }

# sid_to_room -> redis hashmap same thing, key is sid, value is room code. 
# sid_to_room = {
#     # request.sid: roomcode
# }

# def generateRoomCode(length=6):
#     room = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#     # don't want dupes, even though very very rare.
#     while room in rooms:
#         room = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#     return room

# def getNamesInRoom(room):
#     players = rooms[room]['players']
#     names = []
#     for sid in players:
#         names.append(sid_to_player[sid]['name'])
    
#     return names

# def getEmailsInRoom(room):
#     players = rooms[room]['players']
#     names = []
#     for sid in players:
#         names.append(sid_to_player[sid]['email'])
    
#     return names

# # check if everyone in a room has answered the current questions
# def getAnsweredInRoom(room):
#     players = rooms[room]['players']
#     print("CHECKING IF EVERYONE ANSWERED: ", players)
#     # print(players.values())
#     check = all([player['answered'] for player in players.values()])
    
#     return check

# # get scores, format em, sort em and return em for the results screen post-game
# def getScoresInRoom(room):
#     players = rooms[room]['players']

#     scores = []

#     for sid, game_state in players.items():
#         scores.append({'name': sid_to_player[sid]['name'], 'score': game_state['score']})
    
#     # sort by score, descending
#     scores.sort(key=lambda x: x['score'], reverse=True)

#     print(scores)

#     return scores

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
        # REDIS GET ROOM
        # room = sid_to_room.get(request.sid)
        room = getRoom(request.sid)

        # REDIS CHECK ROOM EXISTS
        # if room and room in rooms:
        if room and checkRoomExists(room):
            # REDIS GET PLAYER INFO
            # name = sid_to_player.get(request.sid, {}).get('name')
            name = getPlayerInfo(request.sid)

            leave_room(room)
            # REDIS UPDATE PLAYER COUNT
            # rooms[room]['playerCount'] -= 1
            updatePlayerCount(room, -1)

            self.emit('player_left', {'name': name}, room=room)

            # remove player from room player game state
            # REDIS DELETE PLAYER
            # rooms[room]['players'].pop(request.sid, None)
            deletePlayer(room, request.sid)

            # print('PLAYERS LEFT', rooms[room]['players'])
            print('PLAYERS LEFT', getAllPlayerStatesInRoom(room))

            # if no more players, delete room from dictionary
            # REDIS GET PLAYER COUNT
            # if rooms[room]['playerCount'] <= 0:
            if getPlayerCount(room) <= 0:
                print("DELETING ROOM, NO MORE PLAYERS")
                # REDIS DELETE ROOM
                # rooms.pop(room, None)
                deleteRoom(room)

            # if there are still players check if everyone answered to continue quiz
            # REDIS CHECK ANSWERED IN ROOM
            elif checkAllAnsweredInRoom(room):
                print("SOMEONE LEFT BUT EVERYONE ELSE ANSWERED, CHECKING AND SENDING RESULTS")

                answers = []

                # get names, answers and whether they were correct
                # REDIS GET ALL PLAYER STATES IN ROOM
                # for sid, player_game_state in rooms[room]['players'].items():
                    # username = sid_to_player[sid]['name']
                for player_game_state, username in getAllPlayerStatesInRoom(room):
                    answers.append({
                        "username": username,
                        "user_answer": player_game_state['answer'],
                        "is_correct": player_game_state['correct']
                    })

                    # REDIS RESET ALL ANSWERED IN ROOM
                    # player_game_state['answered'] = False
                
                resetAllAnsweredInRoom(room)

                # REDIS GET QUESTION ID
                # question = Question.getQuestion(rooms[room]['question'])
                question = Question.getQuestion(getQuestionId(room))
                # REDIS GET QUESTION INDEX
                # question_index = rooms[room]['questionIndex']
                question_index = getQuestionIndex(room)
                # send everyones results to everyone
                results = {
                    "correct_answer": question.correct_answer,
                    "question_index": question_index,
                    "answers": answers
                }

                print("EVERYONES RESULTS: ", results)
                # Need to emit list of player resuls to everyone.
                self.emit('answer_checked', results, room=room)

                # REDIS GET QUIZ ID
                # quiz_id = rooms[room]['quiz_id']
                quiz_id = getQuizId(room)
                print('IN QUIZ', quiz_id)
                Thread(target=self.sleepThenContinueQuiz, kwargs={"quiz_id": quiz_id, "room": room}).start()      

        # cleanup disconnected player's entries in sid dictionaries
        # REDIS DELETE PLAYER, called earlier
        # sid_to_player.pop(request.sid, None)
        # sid_to_room.pop(request.sid, None)

    # storing user information after successful connection.
    # client side only needs to send info once, convinient to get info
    # with request sid.
    def on_register_user(self, data):
        # no need to store the same info again
        # REDIS CHECK PLAYER EXISTS
        # if request.sid in sid_to_player:

        print("REGISTERING USERRRRRRR", data)
        if checkPlayerExists(request.sid):
            return

        email = data.get('email')
        name = data.get('name')

        if not email or not name:
            return # error
        
        # REDIS REGISTER PLAYER INFO
        # sid_to_player[request.sid] = {"email": email, "name": name}
        registerPlayerInfo(request.sid, email, name)

        # print('User registered', request.sid, sid_to_player[request.sid])
        print('User registered', request.sid, getPlayerInfo(request.sid))

    # generate room and create a multiplayer room.
    def on_create_room(self):
        # if user info wasn't successfully registered.
        # REDIS CHECK PLAYER EXISTS
        # if request.sid not in sid_to_player:
        if not checkPlayerExists(request.sid):
            return

        # prevent player from creating multiple rooms
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid in sid_to_room:
        if checkPlayerIsInRoom(request.sid):
            return
        
        room = generateRoomId()
        print(room)

        # join socket room, add room to dict with initial game state.
        join_room(room)
        # REDIS CREATE ROOM, REDIS ADD PLAYER TO ROOM
        # rooms[room] = {'players': {request.sid: {'score': 0, 'active': True, 'answered': False, 'answer': '', 'correct': False}}, 
        #                'quiz_id': '',
        #                'questionIndex': 0 ,
        #                'question': None, 
        #                'playerCount': 1, 
        #                'status': 'waiting'}

        createRoom(room)
        
        # easy to get what room a socket is in.
        # REDIS ADD PLAYER TO ROOM
        # sid_to_room[request.sid] = room
        addPlayerToRoom(room, request.sid)

        # send initial update to the lobby creator
        self.emit('room_created', {'code': room}, room=request.sid)
        # self.emit('player_joined', {'names': getNamesInRoom(room)}, room=request.sid)
        self.emit('player_joined', {'names': getAllNamesInRoom(room)}, room=request.sid)
    
    def on_join_room(self, data):
        # if player info was not successfully recorded
        # REDIS CHECK PLAYER EXISTS
        # if request.sid not in sid_to_player:
        if not checkPlayerExists(request.sid):
            return

        # prevent player from joining multiple rooms
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid in sid_to_room:
        if checkPlayerIsInRoom(request.sid):
            return
        
        room = data.get('code')

        # REDIS CHECK ROOM EXISTS
        # if room not in rooms:
        if not checkRoomExists(room):
            return # error room doesnt exist
        
        # add new player game state to room and update room entry and sid_to_room dict
        join_room(room)
        # REDIS ADD PLAYER TO ROOM
        # new_player = {'score': 0, 'active': True, 'answered': False}
        # rooms[room]['players'][request.sid] = new_player
        # sid_to_room[request.sid] = room
        addPlayerToRoom(room, request.sid)

        # REDIS UPDATE PLAYER COUNT
        # rooms[room]['playerCount'] += 1
        updatePlayerCount(room, 1)

        # print(f"players in room {room}", rooms[room]['players'])
        print(f"players in room {room}", getAllPlayerStatesInRoom(room))


        # send room code and list of all players to display on client sides
        self.emit('room_created', {'code': room}, room=request.sid)
        # self.emit('player_joined', {'names': getNamesInRoom(room)}, room=request.sid)
        self.emit('player_joined', {'names': getAllNamesInRoom(room)}, room=request.sid)


    # see if a user is already in a room.
    # if so, send info for room.
    def on_check_for_room(self):
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid not in sid_to_room:
        if not checkPlayerIsInRoom(request.sid):
            self.emit('not_in_room')
            return

        # REDIS GET ROOM
        # room = sid_to_room[request.sid]
        room = getRoom(request.sid)

        self.emit('room_created', {'code': room}, room=request.sid)
        # self.emit('player_joined', {'names': getNamesInRoom(room)}, room=request.sid)
        self.emit('player_joined', {'names': getAllNamesInRoom(room)}, room=request.sid)


    def on_current_players(self):
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid not in sid_to_room:
        if not checkPlayerIsInRoom(request.sid):
            return
        
        # REDIS GET ROOM
        # room = sid_to_room[request.sid]
        room = getRoom(request.sid)

        # reusing the player_joined endpoint because all the times we return names
        # is just for updating client side player list.
        # REDIS GET ALL NAMES IN ROOM
        # self.emit('player_joined', {'names': getNamesInRoom(room)}, room=room)
        self.emit('player_joined', {'names': getAllNamesInRoom(room)}, room=room)

    
    def on_start_game(self, data):
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid not in sid_to_room:
        if not checkPlayerIsInRoom(request.sid):
            return
        
        # REDIS GET ROOM
        # room = sid_to_room[request.sid]
        room = getRoom(request.sid)

        amount = data.get('amount')
        type = data.get('type')
        difficulty = data.get('difficulty')
        category = data.get('category')

        API_URL = f'https://opentdb.com/api.php?amount={amount}&type={type}&difficulty={difficulty}&category={category}'

        response = requests.get(API_URL).json()

        print(response)

        # store the questions in the database, and return the question objects as a list
        questions = store_questions(response['results'])
        
        # create a new multiplayer quiz object and store it in the database
        # set timestamp to the current time since the quiz is just starting
        # create multiplayer participants for all connected users to use 
        # to measure progress
        quiz = MultiplayerQuiz(title=category_dict[category], timestamp=datetime.now(), total_questions=amount, questions=questions)
        quiz.save()

        # REDIS UPDATE QUIZ ID
        # rooms[room]['quiz_id'] = quiz.id
        updateQuizId(room, quiz.id)

        # REDIS GET ALL EMAILS IN ROOM
        # emails = getEmailsInRoom(room)
        emails = getAllEmailsInRoom(room)

        for email in emails:
            # set all the user's active quiz to this one
            user = User.objects(email=email).first()
            print(user.email, user.username)
            user.active_quiz = quiz
            user.save()

            # create MultiplayerParticipants to track quiz progress of each player
            participant = MultiplayerParticipant(user=user)
            quiz.participants.append(participant)
        
        quiz.save()

        quiz_questions = create_quiz_questions(questions)

        print(quiz_questions)
        
        self.emit('start_game', {'questions': quiz_questions}, room=room)
    
    def on_check_answer(self, data):
        # REDIS CHECK PLAYER EXISTS
        # if request.sid not in sid_to_player:
        if not checkPlayerExists(request.sid):
            print("player information not registered")
            return
        
        # REDIS GET PLAYER INFO
        # email = sid_to_player[request.sid]['email']
        email = getPlayerInfo(request.sid)['email']
        user = User.getUser(email=email)
        quiz = user.active_quiz
        question_index = data['question_index']

        # dont check the answer if the user doesn't have an active quiz
        # user.active_quiz can be either Quiz or MultiplayerQuiz so check
        if quiz is None and isinstance(quiz, MultiplayerQuiz):
            print("no active multiplayer quiz")
            return
        
        # players needs to be in a room
        # REDIS CHECK PLAYER IS IN ROOM
        # if request.sid not in sid_to_room:
        if not checkPlayerIsInRoom(request.sid):  
            return
        
        # UPDATE PLAYER GAME STATE
        # REDIS GET ROOM
        # room = sid_to_room[request.sid]
        room = getRoom(request.sid)

        print('CHECK ANSWER GET ALL PLAYER STATES', getAllPlayerStatesInRoom(room))

        # REDIS UPDATE PLAYER STATE
        # player_game_state = rooms[room]['players'][request.sid]
        # player_game_state['answered'] = True
        # player_game_state['answer'] = data['user_answer']
        updatePlayerState(room, request.sid, answer=data['user_answer'], answered=1)

        # get the question object from the question id
        question = Question.getQuestion(data['question_id'])
        # REDIS UPDATE QUESTION ID
        # rooms[room]['question'] = data['question_id']
        updateQuestionId(room, data['question_id'])
        print(question.category)

        # check if the answer is correct
        if data['user_answer'] == question.correct_answer:
            print(question.correct_answer)
            # REDIS UPDATE PLAYER STATE
            # player_game_state['correct'] = True
            
            # scale points to time left
            if data["time_left"] / data["max_time"] > 0.75:
                # REDIS UPDATE PLAYER STATE
                # player_game_state['score'] += 10
                updatePlayerState(room, request.sid, correct=1, score=10)
            else:
                # REDIS UPDATE PLAYER STATE
                # player_game_state['score'] += 10 * (data["time_left"] / data["max_time"])
                updatePlayerState(room, request.sid, correct=1, score=round(10*(data['time_left'] / data['max_time'])))
        else:
            # REDIS UPDATE PLAYER STATE
            # player_game_state['correct'] = False
            updatePlayerState(room, request.sid, correct=0)

        # UPDATE MultiplayerQuiz and MultiplayerParticipant for this user
        participant = quiz.getParticipant(user.id)
        participant.answered_questions.append(AnsweredQuestion(question=question, user_answer=data['user_answer']))
        # participant.score = player_game_state['score']
        participant.score = getPlayerScore(room, request.sid)
        quiz.save()

        # print("results", results)
        # wait until everyone has answered to return results.
        # REDIS CHECK ALL ANSWERED IN ROOM
        # if not getAnsweredInRoom(room):
        if not checkAllAnsweredInRoom(room):
            print("WAITING FOR MORE PLAYERS TO ANSWER")
            return 

        print("EVERYONE ANSWERED, CHECKING AND SENDING RESULTS")
        print('IN QUIZ', quiz)

        answers = []

        # get names, answers and whether they were correct
        # REDIS GET ALL PLAYER STATES IN ROOM
        # for sid, data in rooms[room]['players'].items():
            # username = sid_to_player[sid]['name']
        for data, username in getAllPlayerStatesInRoom(room):
            answers.append({
                "username": username,
                "user_answer": data['answer'],
                "is_correct": data['correct']
            })
        
        resetAllAnsweredInRoom(room)
        
        # send everyones results to everyone
        results = {
            "correct_answer": question.correct_answer,
            "question_index": question_index, # current question index, probably not needed but w/e
            "answers": answers
        }

        print("EVERYONES RESULTS: ", results)
        # Need to emit list of player resuls to everyone.
        self.emit('answer_checked', results, room=room)

        # REDIS GET QUIZ ID
        # Thread(target=self.sleepThenContinueQuiz, kwargs={"quiz_id": rooms[room]['quiz_id'], "room": room}).start()
        Thread(target=self.sleepThenContinueQuiz, kwargs={"quiz_id": getQuizId(room), "room": room}).start()


    def on_leave_room(self):
        # REDIS GET PLAYER INFO
        # name = sid_to_player.get(request.sid, {}).get('name')
        name = getPlayerInfo(request.sid)['email']

        # REDIS GET ROOM
        # room = sid_to_room.get(request.sid)
        room = getRoom(request.sid)

        # REDIS CHECK ROOM EXISTS
        # if room and room in rooms:
        if checkRoomExists(room):
            leave_room(room)
            # REDIS UPDATE PLAYER COUNT
            # rooms[room]['playerCount'] -= 1
            updatePlayerCount(room, -1)

            self.emit('player_left', {'name': name}, room=room)

            # remove player from room player game state
            # REDIS REMOVE PLAYER FROM ROOM
            # rooms[room]['players'].pop(request.sid, None)
            removePlayerFromRoom(room, request.sid)

            # if no more players, delete room from dictionary
            # if rooms[room]['playerCount'] <= 0:
            if getPlayerCount(room) <= 0:
                print("DELETING ROOM, NO MORE PLAYERS")
                # rooms.pop(room, None)
                deleteRoom(room)
        
        # REDIS REMOVE PLAYER FROM ROOM, called earlier
        # sid_to_room.pop(request.sid, None)
        self.emit('leave_room_successful', room=request.sid)
    
    # chat for testing room functionality. may because a feature later
    def on_player_message(self, data):
        message = data.get("message")

        # dont send empty messages
        if not message:
            return # error
        
        # dont send messages if user is not in a room
        # REDIS CHECK PLAYER IN ROOM
        # if request.sid not in sid_to_room:
        if not checkPlayerIsInRoom(request.sid):
            return
        
        # name = sid_to_player[request.sid]['name']
        # room = sid_to_room[request.sid]
        name = getPlayerInfo(request.sid)['name']
        room = getRoom(request.sid)

        self.emit('player_message', {"message" : message, "name": name}, room=room)

    # HELPER FUNCTIONS
    # buffer between sending question results and moving to next question
    # so clients have time to see results
    def sleepThenContinueQuiz(self, quiz_id: str, room: str, seconds: int=2):
        # using quiz_id instead of just sending in the quiz Object itself is because
        # the quiz Object may be stale. Better to get a fresh reference.
        quiz = MultiplayerQuiz.getQuiz(quiz_id)

        sleep(seconds)

        # REDIS GET QUESTION ID
        # if rooms[room]['questionIndex'] != (quiz.total_questions - 1):
        if getQuestionIndex(room) != (quiz.total_questions - 1):
            print('NEXT QUESTION')
            # REDIS INC QUESTION INDEX
            # rooms[room]['questionIndex'] += 1
            incQuestionIndex(room)
            # REDIS GET QUESTION INDEX
            # self.emit('next_question', {"newQuestionIndex": rooms[room]['questionIndex']})
            self.emit('next_question', {"newQuestionIndex": getQuestionIndex(room)})

            return

        # Quiz completed, store results.
        # update participants and store quiz in users that completed the whole thing
        for participant in quiz.getAllParticipants():
            if len(participant.answered_questions) == quiz.total_questions:
                participant.is_finished = True
                user = participant.user
                user.completed_multi_quizzes.append(quiz)

                user.save()
        
        quiz.save()

        # REDIS GET ALL SCORES IN ROOM
        # self.emit('quiz_completed', {"scores": getScoresInRoom(room)}, room=room)
        self.emit('quiz_completed', {"scores": getAllScoresInRoom(room)}, room=room)
