import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router, F

from aiogram.filters import Command, StateFilter

from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.middleware import BaseMiddleware
#from aiogram.fsm.storage.redis import RedisStorage, Redis
import aiogram.utils.markdown as md
from aiogram.enums import ParseMode
import kb, text_phrases, diagnostics, db, config #, buy
import diagnostics_handler, settings_handler, red_button_handler
from storage import storage
from bot import bot
from states import FSMFillForm, FSMsetup, FSMRedButton
import aioschedule

dp: Dispatcher = Router()

async def send_reminder_sleep():
    print('sfklskd')
    await bot.send_message(534311392, '!')


async def scheduler():
    DAY_TIME = "14:12"
    EVERYDAY_TIME = "19:24"
    aioschedule.every().day.at(EVERYDAY_TIME).do(send_reminder_sleep)
    aioschedule.every(1).seconds.do(send_reminder_sleep)
    while 1:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

def schedule_jobs():
    scheduler.add_job(send_reminder_sleep, 'interval',seconds = 5, args = (dp,) )
    print('!!!')



async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начало работы"),
            types.BotCommand("help", 'Помощь'),
            types.BotCommand('diagnostics', 'Диагностика РПП'),
            types.BotCommand("cancel", 'Отмена'),
            types.BotCommand('fillform', 'Анкета'),
            types.BotCommand('red_btn', 'Хочу сорваться'),
            types.BotCommand('buy', 'Купить подпуску на бота'),
            types.BotCommand('settings', 'Настроить бота')
        ]
    )


@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    #asyncio.create_task(scheduler())

    await message.answer(f"Твой ID: {message.from_user.id}")
    #db.drop_db(config.DB_PATH)
    db.create_db(config.DB_PATH)
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

''' 
@dp.message(F.text == text_phrases.menu_red_btn)
async def msg_handler_red_btn(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMRedButton.action_state)
    await message.answer(text = text_phrases.red_btn_start, reply_markup=kb.red_btn_action)
'''
''' 
@dp.message(F.text =='😟 Хочу сорваться', StateFilter(FSMFillForm.show_menu))
async def message_handler_support_before(message: types.Message):
    await message.answer(text = 'Хочу', reply_markup=kb.actions)
'''
@dp.message(F.text =='😨 Сорвался', StateFilter(FSMFillForm.show_menu))
async def message_handler_support_after(message: types.Message):
    await message.answer(text = 'Сорвался', reply_markup=kb.actions)

@dp.message(F.text =='📈 Показать трекеры', StateFilter(FSMFillForm.show_menu))
async def message_handler_tracker(message: types.Message):
    await message.answer(text = 'трекеры', reply_markup=kb.actions)


''' 
@dp.message(, ~StateFilter(default_state))
async def echo(message: types.Message, state:FSMContext):
    await message.answer(f"Твой ID: {message.from_user.id}")
    print(await state.get_state())
'''


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

async def main() -> None:

    # Инициализируем бот и диспетчер
    dp1: Dispatcher = Dispatcher(storage=storage)
    dp1.include_router(dp)
    dp1.include_router(diagnostics_handler.dp)
    dp1.include_router(settings_handler.dp)
    dp1.include_router(red_button_handler.dp)
    logging.basicConfig(level=logging.INFO)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp1.start_polling(bot)


if __name__ == '__main__':\
    asyncio.run(main())
''' 

@dp.callback_query()
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.message.chat.id, 
                             text = callback_query.data)
  
'''                             

'''   
if __name__ == "__main__":
    dp1: Dispatcher = Dispatcher(storage=storage)
    dp1.include_router(dp)
    dp1.include_router(diagnostics_handler.dp)
    dp1.include_router(settings_handler.dp)
    logging.basicConfig(level=logging.INFO)
    dp1.run_polling(bot, skip_updates=True, on_shutdown=shutdown, on_startup=set_default_commands)
    #asyncio.run(main())
'''   