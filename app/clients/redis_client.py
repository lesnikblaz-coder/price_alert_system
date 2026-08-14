import redis
import redis.asyncio as aioredis

from app.config import settings


# sync - used in Celery tasks
sync_redis = redis.from_url(settings.redis_url, decode_responses=True)

# async - FastAPI WebSocket handler
async_redis = aioredis.from_url(settings.redis_url, decode_responses=True)