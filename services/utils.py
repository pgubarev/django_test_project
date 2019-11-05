from requests import post, put
from signals.celery import celery_app


@celery_app.task
def send_post_message(url, data):
    post(url=url, headers={'content-type': 'application/json'}, json=data)


@celery_app.task
def send_put_message(url, data):
    put(url=url, headers={'content-type': 'application/json'}, json=data)

