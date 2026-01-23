from src.config.celery_app import celery_app


@celery_app.task
def example_task(x, y):
    return x + y


@celery_app.task
def example_task2(x, y):
    return x + y
