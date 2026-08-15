import asyncio

from app.repositories.alert_repo import AlertRepository
from app.services.price_service import PriceService
from app.workers.celery_app import celery_app
from app.services.alert_worker_service import AlertWorkerService
from app.clients.redis_client import sync_redis
from app.database import AsyncSessionLocal
from app.config import settings
from app.logging_config import logger


@celery_app.task(name="app.workers.tasks.check_prices")
def check_prices():
    asyncio.run(_check_prices())

async def _check_prices():
    async with AsyncSessionLocal() as session:
        alert_repo = AlertRepository(session)

        async with PriceService.create(settings.fhub_api_key) as price_service:
            service = AlertWorkerService(
                alert_repo=alert_repo,
                price_service=price_service,
                redis=sync_redis
            )

            await service.check_prices()

    logger.info("Price check task complete")