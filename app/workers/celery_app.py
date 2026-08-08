from celery import Celery

celery_app = Celery(
    "price_alerts",
    broker="redis://redis:6379/0", # Redis database 0 for the queue
    backend="redis://redis:6379/1", # Redis database 1 for the task results
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    # only acknowledge a task as "done" after it finishes
    # if worker crashes mid-task, Redis keeps the message and retries
    task_acks_late=True,

    # don't grab the next task before finishing the current one
    worker_prefetch_multiplier=1,

    # beat schedule - what runs and how ofter
    beat_schedule={
        "check-price-every-60-seconds": {
            "task": "app.workers.tasks.check_prices",
            "schedule": 60
        }
    }
)