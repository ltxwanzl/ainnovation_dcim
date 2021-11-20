import redis
from django.conf import settings


redis_host = settings.TASKS_REDIS_HOST
redis_db = settings.TASKS_REDIS_DATABASE
redis_port = settings.TASKS_REDIS_PORT
redis_password = settings.TASKS_REDIS_PASSWORD

POOL = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_password, max_connections=1000)

