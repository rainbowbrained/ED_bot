import asyncio
import logging

from aiogram import executor
import handlers


if __name__ == "__main__":
    executor.start_polling(handlers.dp, loop = handlers.loop)
