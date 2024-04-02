# your_app/tasks.py

from celery import shared_task
import json
import redis

@shared_task
def send_sms_task(phone_number, message):
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # Enqueue SMS task to the message queue
    task_data = json.dumps({'phone_number': phone_number, 'message': message})
    redis_client.lpush('sms_tasks', task_data)