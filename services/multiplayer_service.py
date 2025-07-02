from redis_client import redis_client as rc
import random
import string
import json

# room:code
# room:code:players
# room:code:player:sid
# sid_to_player
# sid_to_room

def generateRoomId(length=6):
    room_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # don't want dupes, even though very very rare.
    while checkRoomExists(room_id):
        room_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    return room_id

# for redis hash names
def getRoomHash(room_id):
    return ':'.join(['room', room_id])

def getRoomPlayersHash(room_id):
    return ':'.join(['room', room_id, 'players'])

def getPlayerHash(room_id, sid):
    return ':'.join(['room', room_id, 'player', sid])

def getRoom(sid):
    return rc.hget("sid_to_room", sid)

def createRoom(room_id):
    rc.hset(getRoomHash(room_id), mapping={
        'quiz_id': '', 
        'question_id': '', 
        'question_index': 0,
        'player_count': 1,
        'started': 0
    })

def getQuizId(room_id):
    return rc.hget(getRoomHash(room_id), 'quiz_id')

def getQuestionId(room_id):
    return rc.hget(getRoomHash(room_id), 'question_id')

def getQuestionIndex(room_id):
    return int(rc.hget(getRoomHash(room_id), 'question_index'))

def updateQuizId(room_id, quiz_id):
    rc.hset(getRoomHash(room_id), 'quiz_id', str(quiz_id))

def updateQuestionId(room_id, question_id):
    rc.hset(getRoomHash(room_id), 'question_id', question_id)

def incQuestionIndex(room_id):
    print("CURRENT ROOM STATE :", rc.hgetall(getRoomHash(room_id)))
    print("CURRENT PLAYERS :", rc.smembers(getRoomPlayersHash(room_id)))
    print("PLAYER COUNT", rc.hget(getRoomHash(room_id), 'player_count'))

    rc.hincrby(getRoomHash(room_id), 'question_index', 1)

def addPlayerToRoom(room_id, sid):
    # player game state
    rc.hset(getPlayerHash(room_id, sid), mapping={'score': 0, 'answer': '', 'answered': 0, 'correct': 0})

    # room players list
    rc.sadd(getRoomPlayersHash(room_id), sid)

    # sid to room
    rc.hset("sid_to_room", sid, room_id)

def removePlayerFromRoom(room_id, sid):
    rc.delete(getPlayerHash(room_id, sid))

    rc.srem(getRoomPlayersHash(room_id), sid)

    rc.hdel("sid_to_room", sid)

def checkRoomExists(room_id):
    return rc.exists(getRoomHash(room_id))

def registerPlayerInfo(sid, email, name):
    return rc.hset("sid_to_player", sid, json.dumps({'email': email, 'name': name}))

def checkPlayerExists(sid):
    return rc.hexists("sid_to_player", sid)

def checkPlayerIsInRoom(sid):
    return rc.hexists("sid_to_room", sid)

def getPlayerInfo(sid):
    return json.loads(rc.hget("sid_to_player", sid))

def getAllNamesInRoom(room_id):
    # get all sids in room from the room:code:players set
    sids = rc.smembers(getRoomPlayersHash(room_id))

    # use sids to get player info from sid_to_player using a pipeline
    # to issue all the commands at once and get all the results back in 1 array
    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hget('sid_to_player', sid)
    
    players_data = pipeline.execute()
    
    return [json.loads(player)['name'] for player in players_data]

def getAllEmailsInRoom(room_id):
    # get all sids in room from the room:code:players set
    sids = rc.smembers(getRoomPlayersHash(room_id))

    # use sids to get player info from sid_to_player using a pipeline
    # to issue all the commands at once and get all the results back in 1 array
    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hget('sid_to_player', sid)
    
    players_data = pipeline.execute()
    
    return [json.loads(player).get('email', None) for player in players_data]

def checkAllAnsweredInRoom(room_id):
    # get all sids in room from the room:code:players set
    sids = rc.smembers(getRoomPlayersHash(room_id))

    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hget(getPlayerHash(room_id, sid), "answered")

    results = pipeline.execute()

    # redis doesnt support booleans so im using 0 and 1 instead.
    return all([answered == '1' for answered in results])

def getAllScoresInRoom(room_id):
    # get all sids in room from the room:code:players set
    sids = rc.smembers(getRoomPlayersHash(room_id))

    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hget("sid_to_player", sid) # email, name, etc.
        pipeline.hget(getPlayerHash(room_id, sid), "score") # score
    
    results = pipeline.execute()

    scores = []
    # step of 2 because i0 will be player json and i1 will be player score.
    for i in range(0, len(results), 2):
        name = json.loads(results[i]).get('name', None)
        score = results[i+1]

        scores.append({'name': name, 'score': score})
    
    scores.sort(key=lambda x: x['score'], reverse=True)

    return scores

def getPlayerScore(room_id, sid):
    return int(rc.hget(getPlayerHash(room_id, sid), 'score'))

def updatePlayerState(room_id, sid, score=None, answer=None, answered=None, correct=None):
    pipeline = rc.pipeline()
    
    player_state_hash = getPlayerHash(room_id, sid)

    if score is not None:
        pipeline.hincrby(player_state_hash, 'score', score)

    if answer is not None:
        pipeline.hset(player_state_hash, 'answer', answer)

    if answered is not None:
        pipeline.hset(player_state_hash, 'answered', answered)
    
    if correct is not None:
        pipeline.hset(player_state_hash, 'correct', correct)
    
    pipeline.execute()

def resetAllAnsweredInRoom(room_id):
    sids = rc.smembers(getRoomPlayersHash(room_id))

    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hset(getPlayerHash(room_id, sid), 'answered', 0)
    
    pipeline.execute()

def getAllPlayerStatesInRoom(room_id):
    sids = rc.smembers(getRoomPlayersHash(room_id))

    pipeline = rc.pipeline()

    for sid in sids:
        pipeline.hgetall(getPlayerHash(room_id, sid))
    
    states = pipeline.execute()

    for sid in sids:
        pipeline.hget("sid_to_player", sid)
    
    player_infos = pipeline.execute()

    print("SIDS, STATES, PLAYER_INFOS", states, player_infos)

    results = []
    for state, info in zip(states, player_infos):
        print("PLAYER STATES: ", state, info)
        results.append((state, json.loads(info)['name']))
    
    return results

def updatePlayerCount(room_id, amount):
    rc.hincrby(getRoomHash(room_id), "player_count", amount) 

def getPlayerCount(room_id):
    return int(rc.hget(getRoomHash(room_id), "player_count"))

def deletePlayer(room_id, sid):
    # delete individual player gamestate hash
    rc.delete(getPlayerHash(room_id, sid))

    # delete player from room
    rc.srem(getRoomPlayersHash(room_id), sid)

    # delete player from sid_to_room
    rc.hdel("sid_to_room", sid)

    # delete player from sid_to_player
    rc.hdel("sid_to_player", sid)

def deleteRoom(room_id):
    rc.delete(getRoomHash(room_id))