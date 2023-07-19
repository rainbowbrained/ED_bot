
from aiogram import  types, Router, F

from aiogram.filters import Command, StateFilter
import random

from aiogram.fsm.context import FSMContext
import kb, text_phrases
from bot import bot
from states import FSMRedButton
from storage import storage

callback_feeling_dict = {
    'anger' : text_phrases.red_btn_feeling2,
    'anxiety' : text_phrases.red_btn_feeling1,
    'happy' :  text_phrases.red_btn_feeling4,
    'shame' :  text_phrases.red_btn_feeling3,
    'sadness' :  text_phrases.red_btn_feeling5,
    'boredom' :  text_phrases.red_btn_feeling6,
    'other' :  ''
}


dp = Router()

@dp.message(Command('red_btn'))
@dp.message(F.text == text_phrases.menu_red_btn)
async def msg_handler_red_btn(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMRedButton.action_state)
    await message.answer(text = text_phrases.red_btn_start, reply_markup=kb.red_btn_action)


@dp.callback_query(StateFilter(FSMRedButton.action_state))
async def callback_handler_action(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'ok':  #выходим в меню
        i = random.randint(0, len(text_phrases.red_btn_success)-1)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_success[i], 
                                   reply_markup=kb.actions)
        await state.clear()

    elif callback_query.data == 'other':  
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_action_other1)
    else:
        await state.update_data(action = callback_query.data )
        await state.set_state(FSMRedButton.feeling_state)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_felling, 
                                   reply_markup=kb.red_btn_feeling)


@dp.message(StateFilter(FSMRedButton.action_state))
async def msg_handler_action(message: types.Message, state: FSMContext):
    await state.update_data(action = message.text)
    await message.delete()
    await message.answer(text = text_phrases.red_btn_felling, reply_markup=kb.red_btn_feeling)
    await state.set_state(FSMRedButton.feeling_state)

@dp.callback_query(StateFilter(FSMRedButton.feeling_state))
async def callback_handler_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)

    if callback_query.data == 'other':  
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_feeling_other1)
    else:
        await state.update_data(feeling = callback_query.data )
        await state.set_state(FSMRedButton.intencity_state)
        #await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_reminder.format(feeling = callback_query.data))
        
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_intencity)
        
        #i = random.randint(0, len(text_phrases.red_btn_better_question)-1)
        
        #await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_better_question[i], 
        #                           reply_markup=kb.answers_yes_no)



@dp.message(StateFilter(FSMRedButton.feeling_state))
async def msg_handler_feeling(message: types.Message, state: FSMContext):
    await state.update_data(feeling = message.text)
    await message.delete()
    await state.set_state(FSMRedButton.intencity_state)
    await message.answer(text_phrases.red_btn_intencity)
        
    #i = random.randint(0, len(text_phrases.red_btn_better_question)-1)
    #await message.answer(text_phrases.red_btn_better_question[i], 
    #                               reply_markup=kb.answers_yes_no)


@dp.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10, 
            StateFilter(FSMRedButton.intencity_state))
async def msg_handler_intencity(message: types.Message, state: FSMContext):
    # Update state and data
    await message.delete()
    await state.set_state(FSMRedButton.better_state)
    await state.update_data(intencity =  int(message.text))
    feel = await state.get_data()
    feel = feel['feeling']
    await message.answer(text_phrases.red_btn_reminder.format(feeling = callback_feeling_dict[feel]))
    i = random.randint(0, len(text_phrases.red_btn_better_question)-1)
    await message.answer(text_phrases.red_btn_better_question[i], 
                                   reply_markup=kb.answers_yes_no_some)

@dp.message(StateFilter(FSMRedButton.intencity_state))
async def msg_handler_intencity(message: types.Message, state: FSMContext):
    # Update state and data
    await message.delete()
    await message.answer(text_phrases.red_btn_intencity_fail)


@dp.callback_query(StateFilter(FSMRedButton.better_state))
async def callback_handler_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)

    if callback_query.data == 'yes':  
        i = random.randint(0, len(text_phrases.red_btn_success)-1)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_success[i])
        feel = await state.get_data()
        print(feel)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_post_success.format(feeling = feel['feeling']))
        await state.set_state(FSMRedButton.post_better_state)
    else:
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_practice_start)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_practice)
        i = random.randint(0, len(text_phrases.red_btn_better_question)-1)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_better_question[i], 
                                   reply_markup=kb.answers_yes_no)
        

@dp.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10, 
            StateFilter(FSMRedButton.post_better_state))
async def msg_handler_intencity(message: types.Message, state: FSMContext):
    # Update state and data
    await message.delete()
    new_intencity = int(message.text)
    old_intencity = await state.get_data()
    old_intencity = old_intencity['intencity']
    feel = await state.get_data()
    feel = feel['feeling']
    if old_intencity > new_intencity:
        await message.answer(text_phrases.red_btn_before_after_dec.format(feeling = feel, before = old_intencity, after = new_intencity), 
        reply_markup=kb.answers_red_btn_yes_no_)
    elif old_intencity < new_intencity:
        await message.answer(text_phrases.red_btn_before_after_inc.format(feeling = feel, before = old_intencity, after = new_intencity), 
        reply_markup=kb.answers_red_btn_yes_no_)
    else: 
        await message.answer(text_phrases.red_btn_before_after_same.format(feeling = feel, before = old_intencity), 
        reply_markup=kb.answers_red_btn_yes_no_)
    await state.update_data(intencity =  new_intencity)


@dp.callback_query(StateFilter(FSMRedButton.post_better_state))
async def callback_handler_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)

    if callback_query.data == 'no':  
        i = random.randint(0, len(text_phrases.red_btn_success)-1)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_success[i], reply_markup=kb.actions)
        await state.clear()
    else:
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_practice_start)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_practice)
        await state.set_state(FSMRedButton.better_state)
        i = random.randint(0, len(text_phrases.red_btn_better_question)-1)
        await bot.send_message(callback_query.from_user.id, text_phrases.red_btn_better_question[i], 
                                   reply_markup=kb.answers_yes_no)
        

@dp.message()
async def echo(message: types.Message, state:FSMContext):
    await message.answer(f"Твой ID: {message.from_user.id}")
    print(await state.get_state())

''' 
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
'''