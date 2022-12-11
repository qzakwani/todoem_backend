# import redis
# import json

# class RedisDB(redis.Redis):
    
#     def get_data(self, key: str) -> str:
#         res = super().get(key)
#         if res is None: 
#             return None
#         return json.loads(res)


# r_db = RedisDB(host='localhost', port=6379)