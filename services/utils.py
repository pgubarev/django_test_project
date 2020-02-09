import requests
import logging

from signals.celery import celery_app

logger = logging.getLogger('tasks')


@celery_app.task
def send_post_message(url, data):
    logger.info('try to send post message: {} - {}'.format(url, data))
    try:
        response = requests.post(
            url=url, headers={'content-type': 'application/json'}, json=data
        )
        logger.info(
            'post request was sent: {} - {}'.format(url, response.status_code)
        )
    except Exception as ex:
        logger.info(
            'error during sending post request: {} - {}'.format(url, ex)
        )


@celery_app.task
def send_put_message(url, data):
    logger.info('try to send put message: {} - {}'.format(url, data))
    try:
        response = requests.put(
            url=url, headers={'content-type': 'application/json'}, json=data
        )
        logger.info(
            'put request was sent: {} - {}'.format(url, response.status_code)
        )
    except Exception as ex:
        logger.info(
            'error during sending put request: {} - {}'.format(url, ex)
        )
