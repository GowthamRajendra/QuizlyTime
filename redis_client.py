from redis import Redis

# set up redis for multiplayer game handling
redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)