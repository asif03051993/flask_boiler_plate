""" User async tasks """
import logging
import datetime
import json

from app import celery
from cache import cache

CELERY_QUEUE = 'queue1'

def schedule_otp_generation_for_user(user_id, **kwargs):
    """schedule_otp_generation_for_user."""
    params = dict(userId=user_id)
    eta = datetime.datetime.now() + datetime.timedelta(
        seconds=1)
    return generate_otp_for_user.apply_async(
        queue=CELERY_QUEUE,
        args=[params], eta=eta)


@celery.task(bind=True, default_retry_delay=3, max_retries=3)
def generate_otp_for_user(self, request_data):
    """generate_otp_for_user."""

    user_id = request_data.get('userId', None)
    logging.info('Generating otp for user => {0} fe_id'.format(user_id))

    assert user_id, 'user_id not provided!'


