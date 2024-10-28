import aioredis
from config import REDIS_HOST, REDIS_PORT

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


redis = aioredis.from_url(REDIS_URL, decode_responses=True)
