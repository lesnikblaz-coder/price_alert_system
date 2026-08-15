import redis

from app.config import settings


# sync - used in Celery tasks
sync_redis = redis.from_url(settings.redis_url, decode_responses=True)