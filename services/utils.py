import requests
from signals.celery import celery_app


@celery_app.task
def send_post_message(url, data):
    requests.post(url=url, headers={'content-type': 'application/json'}, json=data)


@celery_app.task
def send_put_message(url, data):
    requests.put(url=url, headers={'content-type': 'application/json'}, json=data)

