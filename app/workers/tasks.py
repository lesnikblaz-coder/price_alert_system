from app.workers.celery_app import celery_app
from app.logging_config import logger

@celery_app.task(name="app.workers.tasks.check_prices")
def check_prices():
    logger.info("Price check task running")
    # just verifying this runs