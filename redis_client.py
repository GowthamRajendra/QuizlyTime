from redis import Redis, exceptions
import os

# set up redis for multiplayer game handling
redis_client = None

# call after envs are loaded
def init_redis():
    global redis_client
    print("REDIS_CLIENT HOST ", os.getenv("REDIS_HOST"))
    redis_client = Redis(host=os.getenv("REDIS_HOST", "localhost"), 
                         port=6379, 
                         db=0, 
                         decode_responses=True)
    
    try:
        if redis_client.ping():
            print("Connected to Redis!")
        else:
            print("Redis server did not response to ping.")
    except exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")

# def get_redis_client():
#     if redis_client is None:
#         raise RuntimeError("Redis client not initialized. Call init_redis() first.")
#     return redis_client
