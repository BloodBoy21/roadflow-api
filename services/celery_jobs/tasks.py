from lib.celery import celery_app


@celery_app.task(bind=True, name="agents.hello")
def hello(self):
    print("hello world")
