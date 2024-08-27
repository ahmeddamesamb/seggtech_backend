# utils/redis_client.py
import redis
from django.conf import settings

# Configurez le client Redis en utilisant les paramètres de votre settings.py
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)
