from redis import Redis
import os

# set up redis for multiplayer game handling
redis_client = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)