from flask_socketio import Namespace, emit, join_room, leave_room
from flask import request
import random
import string
'''
multiplayer rooms, for now is an in-memory dict, later will be redis because docker backends.

player's game state is stored in their respective rooms, but other information about the player
like what room they are in or what their name are located in sid_to_player and sid_to_room
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

def getPlayersInRoom(room):
    players = rooms[room]['players']
    names = []
    for sid in players:
        names.append(sid_to_player[sid]['name'])
    
    return names

class MultiplayerNamespace(Namespace):
    def on_connect(self):
        print('multiplayer connection established')
        print(request.sid)

    # clean up dictionary entries on disconnection of any kind.
    # # TODO, reconnecting
    def on_disconnect(self):
        print("BEFFFFFFFFOOOOOOOOOOOREEEEEEEE")
        print('multiplayer connection terminated')
        print(sid_to_player, sid_to_room, rooms)
        
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

        print(sid_to_player, sid_to_room, rooms)
        print("AAAAAFFFFFFFFTTTTTTTEEEEEEEEEEERRRRRRRRR")


    # storing user information after successful connection.
    # client side only needs to send info once, convinient to get info
    # with request sid.
    def on_register_user(self, data):
        email = data.get('email')
        name = data.get('name')

        if not email or not name:
            return # error
        
        sid_to_player[request.sid] = {"email": email, "name": name}

        print('User registered', request.sid, sid_to_player[request.sid])

    # generate room and create a multiplayer room.
    # TODO, browse lobby screen?
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
        rooms[room] = {'players': {request.sid: {'score': 0, 'active': True, 'answered': False}}, 'playerCount': 1, 'status': 'waiting'}
        
        # easy to get what room a socket is in.
        sid_to_room[request.sid] = room

        # send initial update to the lobby creator
        self.emit('room_created', {'code': room}, room=room)
        self.emit('player_joined', {'names': getPlayersInRoom(room)}, room=room)
    
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
        self.emit('player_joined', {'names': getPlayersInRoom(room)}, room=room)
    
    # get current players in the room.
    def on_current_players(self):
        if request.sid not in sid_to_room:
            return
        
        room = sid_to_room[request.sid]

        self.emit('player_joined', {'names': getPlayersInRoom(room)}, room=room)
    
    def on_leave_room(self):
        print("BEFFFFFFFFOOOOOOOOOOOREEEEEEEE")
        print('Leaving room...')
        print(sid_to_player, sid_to_room, rooms)

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

        print(sid_to_player, sid_to_room, rooms)
        print("AAAAAFFFFFFFFTTTTTTTEEEEEEEEEEERRRRRRRRR")


    
    # testing room functionality. working so far. perhaps add a full chat feature later.
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


        

