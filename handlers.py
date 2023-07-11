import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F

from aiogram.filters import Command, StateFilter

from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.middleware import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage, Redis
import aiogram.utils.markdown as md
from aiogram.enums import ParseMode
import kb, text_phrases, diagnostics, db, config #, buy
import diagnostics_handler, settings_handler
from bot import bot
from states import FSMFillForm, FSMsetup

# Инициализируем Redis
redis: Redis = Redis(host=config.HOST_STORAGE)
storage: RedisStorage = RedisStorage(redis=redis)

#bot: Bot = Bot(token=config.BOT_TOKEN)
#dp = Dispatcher(bot, storage=storage)
dp: Dispatcher = Router()


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начало работы"),
            types.BotCommand("help", 'Помощь'),
            types.BotCommand('diagnostics', 'Диагностика РПП'),
            types.BotCommand("cancel", 'Отмена'),
            types.BotCommand('fillform', 'Анкета'),
            types.BotCommand('buy', 'Купить подпуску на бота'),
            types.BotCommand('settings', 'Настроить бота')
        ]
    )


@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    db.drop_db(config.DB_PATH)
    db.create_db(config.DB_PATH)
    # Сбрасываем состояние
    await state.clear()
    name = message.from_user.full_name
    await message.answer(text_phrases.greet.format(name=name))
    
    await state.update_data(name = name)
    #await message.delete()
    if not db.user_in_db(message.from_user.id):
        db.add_user_to_db(message.from_user.id, name)
        await message.answer(text_phrases.greet_get_acquainted)
        await message.answer(text = '1. Выбери свой пол', reply_markup=kb.gender)
        await state.set_state(FSMFillForm.fill_gender)
    else:
        await state.set_state(FSMFillForm.show_menu)
        await bot.send_message(message.from_user.id, text_phrases.greet_already_acquainted, 
                                   reply_markup=kb.actions)
            
# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: types.Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@dp.message(Command('cancel'), StateFilter(default_state))
async def process_cancel_command(message: types.Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')

@dp.message(Command('test'), StateFilter(default_state))
async def test_command(message: types.Message, state: FSMContext):
    await message.answer('1')
    print(await state.get_state())


@dp.message(Command('help'))
async def start_command(message: types.Message):
    await message.reply(text=text_phrases.HELP_COMMAND, parse_mode='HTML')

@dp.message(Command('diagnostics'), StateFilter(FSMFillForm.__all_states__))
async def start_command(message: types.Message, state:FSMContext):
    await message.answer("Хотите пройти диагностику?", reply_markup=kb.answers_yes_no)
    await state.set_state(FSMFillForm.fill_diagnostics0)
    
@dp.message(F.text =='💧 Попил воды', StateFilter(FSMFillForm.show_menu))
async def message_handler_water(message: types.Message):
    await message.answer(text = 'Попил воды', reply_markup=kb.actions)

@dp.message(F.text =='🥦 Поел', StateFilter(FSMFillForm.show_menu))
async def message_handler_food(message: types.Message):
    await message.answer(text = 'Поел')

@dp.message(F.text =='😟 Хочу сорваться', StateFilter(FSMFillForm.show_menu))
async def message_handler_support_before(message: types.Message):
    await message.answer(text = 'Хочу', reply_markup=kb.actions)

@dp.message(F.text =='😨 Сорвался', StateFilter(FSMFillForm.show_menu))
async def message_handler_support_after(message: types.Message):
    await message.answer(text = 'Сорвался', reply_markup=kb.actions)

@dp.message(F.text =='📈 Показать трекеры', StateFilter(FSMFillForm.show_menu))
async def message_handler_tracker(message: types.Message):
    await message.answer(text = 'трекеры', reply_markup=kb.actions)

@dp.message(StateFilter(default_state))
async def echo(message: types.Message):
    await message.answer(f"Твой ID: {message.from_user.id}")
    


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

''' 
async def main():
    dispatcher = Dispatcher()
    dispatcher.startup.register(set_default_commands)
    dispatcher.shutdown.register(shutdown)
    dispatcher.storage = storage
    dispatcher.include_router(dp)
    await dispatcher.start_polling(bot)
'''

# Функция конфигурирования и запуска бота
''' 
async def main() -> None:

    # Инициализируем бот и диспетчер
    #bot: Bot = Bot(token=config.BOT_TOKEN)
    dp1: Dispatcher = Dispatcher(storage=storage)
    dp1.include_router(dp)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp1.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
''' 
''' 
@dp.callback_query()
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.message.chat.id, 
                             text = callback_query.data)
  
'''                             


if __name__ == "__main__":
    dp1: Dispatcher = Dispatcher(storage=storage)
    dp1.include_router(dp)
    dp1.include_router(diagnostics_handler.dp)
    dp1.include_router(settings_handler.dp)
    logging.basicConfig(level=logging.INFO)
    dp1.run_polling(bot, skip_updates=True, on_shutdown=shutdown, on_startup=set_default_commands)
    #asyncio.run(main())
