
from aiogram.fsm.storage.redis import RedisStorage, Redis
import config 

# Инициализируем Redis
redis: Redis = Redis(host=config.HOST_STORAGE)
storage: RedisStorage = RedisStorage(redis=redis)
