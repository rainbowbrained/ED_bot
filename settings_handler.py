
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
@dp.message(F.text == text_phrases.menu_settings)
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
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'yes': #отслеживать воду
        await state.update_data(check_water = 1)
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_water_reminder_yes_no, 
                                   reply_markup=kb.drink_water_reminder)
        await state.set_state(FSMsetup.setup_functions_water_reminder)
    else: #не отслеживать воду. отслеживать сон?
        await state.update_data(check_water = 0)
        await state.set_state(FSMsetup.setup_functions_sleep)
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_functions_sleep, 
                                   reply_markup=kb.answers_yes_no)
        
# сколько раз когда пить воду? 
@dp.message(StateFilter(FSMsetup.setup_functions_water_reminder))
async def callback_handler_diagnose1(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text != 'Выключить напоминания': #отслеживать воду
        await state.update_data(water_reminder = message.text)
    await state.set_state(FSMsetup.setup_functions_sleep)
    await  message.answer(text_phrases.setup_functions_sleep, 
                                   reply_markup=kb.answers_yes_no)
        

@dp.callback_query(StateFilter(FSMsetup.setup_functions_sleep))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'yes': #отслеживать сон
        await state.update_data(check_sleep= 1)
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_sleep_reminder_yes_no, 
                                   reply_markup=kb.answers_yes_no)
        await state.set_state(FSMsetup.setup_functions_sleep_reminder)
    else: #не отслеживать сон
        await state.update_data(check_sleep= 0)
        print(await state.get_data())
        await state.set_state(FSMFillForm.show_menu)
        txt = await generate_text_settings(state)
        await bot.send_message(callback_query.from_user.id, txt, 
                                   reply_markup=kb.actions)


@dp.callback_query(StateFilter(FSMsetup.setup_functions_sleep_reminder))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)  
    if callback_query.data == 'yes': #отслеживать сон
        await state.update_data(check_sleep= 1)
        await bot.send_message(callback_query.from_user.id, text_phrases.setup_sleep_reminder_time, 
                                   reply_markup=kb.sleep_reminder)
    else: #не отслеживать сон
        await state.update_data(check_sleep= 0)
        print(await state.get_data())
        await state.set_state(FSMFillForm.show_menu)
        txt = await generate_text_settings(state)
        await bot.send_message(callback_query.from_user.id, txt, 
                                   reply_markup=kb.actions)
        await state.clear()
        
# когда напоминать о сне?
@dp.message(StateFilter(FSMsetup.setup_functions_sleep_reminder))
async def callback_handler_diagnose1(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text != 'Выключить напоминания': #отслеживать воду
        await state.update_data(sleep_reminder = message.text)
    print(await state.get_data())
    txt = await generate_text_settings(state)
    await  message.answer(txt, reply_markup=kb.actions)
    await state.clear()

async def generate_text_settings(state: FSMContext):
    s = await state.get_data()
    print(s)
    if s['check_water']:
        water = 'да'
    else:
        water = 'нет'
    if s['check_sleep']:
        sleep = 'да'
    else:
        sleep = 'нет'

    if 'water_reminder' in s:
        water_freq = 'каждые '
        water_freq += s['water_reminder']
    else: 
        water_freq = 'нет'
    
    if 'sleep_reminder' in s:
        sleep_time = 'в '
        sleep_time += s['sleep_reminder']
    else: 
        sleep_time = 'нет '
    return text_phrases.setup_final.format(water=water, sleep=sleep, water_freq=water_freq, sleep_time=sleep_time)
