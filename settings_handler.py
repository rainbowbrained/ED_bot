
from aiogram import  types, Router, F

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

dp = Router()

@dp.message(Command('settings'))
@dp.message(F.text == text_phrases.btn_start_programm, StateFilter(FSMsetup.setup_functions0))
async def message_handler_support_before(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(text = text_phrases.setup_functions, reply_markup=kb.setup_functions)
    await state.set_state(FSMsetup.setup_functions0)
    

@dp.callback_query(StateFilter(FSMsetup.setup_functions0))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'yes': #настраиваем бота
        #отслеживать воду?
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_functions_water, 
                                   reply_markup=kb.answers_yes_no)
        await state.set_state(FSMsetup.setup_functions_water)
    else: #выходим в меню
        await state.set_state(FSMFillForm.show_menu)
        await bot.send_message(callback_query.from_user.id, text_phrases.menu, 
                                   reply_markup=kb.actions)

@dp.callback_query(StateFilter(FSMsetup.setup_functions_water))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes': #отслеживать воду
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_water_reminder_yes_no, 
                                   reply_markup=kb.drink_water_reminder)
        await state.set_state(FSMsetup.setup_functions_water_reminder)
    else: #не отслеживать воду. отслеживать сон?
        await state.set_state(FSMsetup.setup_functions_sleep)
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_functions_sleep, 
                                   reply_markup=kb.answers_yes_no)
        
# сколько раз когда пить воду? 
@dp.message(StateFilter(FSMsetup.setup_functions_water_reminder))
async def callback_handler_diagnose1(message: types.Message, state: FSMContext):
    if message.text == 'yes': #отслеживать воду
        await message.answer('!')
    await state.set_state(FSMsetup.setup_functions_sleep)
    await  message.answer(text_phrases.setup_functions_sleep, 
                                   reply_markup=kb.answers_yes_no)
        

@dp.callback_query(StateFilter(FSMsetup.setup_functions_sleep))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes': #отслеживать сон
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_sleep_reminder_yes_no, 
                                   reply_markup=kb.answers_yes_no)
        await state.set_state(FSMsetup.setup_functions_water_reminder)
    else: #не отслеживать воду. отслеживать сон?
        await state.set_state(FSMFillForm.show_menu)
        await bot.send_message(callback_query.from_user.id, 'penis', 
                                   reply_markup=kb.actions)
