# анкета и диагностика
from aiogram import types, Router, F

from aiogram.filters import Command, StateFilter

from aiogram.fsm.context import FSMContext
import aiogram.utils.markdown as md
from aiogram.enums import ParseMode
import kb, text_phrases, diagnostics, db
from states import FSMFillForm, FSMsetup
from bot import bot

dp = Router()


@dp.message(Command('diagnostics'))
async def start_diagnostics(message: types.Message, state:FSMContext):
    await message.delete()
    await message.answer(text_phrases.offer_diagnostics, reply_markup=kb.answers_yes_no)
    await state.set_state(FSMFillForm.fill_diagnostics0)

# ----------------------------------------- Check gender

@dp.callback_query(StateFilter(FSMFillForm.fill_gender))
async def callback_handler_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'gender_man':
        await bot.send_message(callback_query.from_user.id, '1. Пол мужской')
        gender = 'мужской'
    elif callback_query.data == 'gender_woman':
        await bot.send_message(callback_query.from_user.id, '1. Пол женский')
        gender = 'женский'
    else:
        await bot.send_message(callback_query.from_user.id, '1. Пол небинарный')
        gender = 'небинарный'
    await state.update_data(gender = gender)
    await bot.send_message(callback_query.from_user.id, '2. Введи свой возраст', reply_markup=kb.do_not_answer)
    await state.set_state(FSMFillForm.fill_age)

@dp.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_education(message: types.Message):
    await message.answer(text=text_phrases.use_buttons)

# ----------------------------------------- Check age. Age gotta be digit
@dp.message(lambda message: message.text.isdigit() and 4 <= int(message.text) <= 120, StateFilter(FSMFillForm.fill_age))
async def message_handler_age(message: types.Message, state: FSMContext):
    # Update state and data
    await state.set_state(FSMFillForm.fill_height)
    age = int(message.text)
    msg = '3. Введи свой рост'
    await message.answer(text = msg, reply_markup=kb.do_not_answer)
    await state.update_data(age = age)

@dp.message(StateFilter(FSMFillForm.fill_age))
async def message_handler_age_failed(message: types.Message, state: FSMContext):
    if message.text == "Не знаю/не хочу указывать":
        await message.reply("Хорошо. Возраст можно не указывать или указать позже")
        await state.update_data(age = None)
        await state.set_state(FSMFillForm.fill_height)
        await message.answer(text = '3. Введи свой рост', reply_markup=kb.do_not_answer)
    else:
        return await message.reply("Возраст должен быть целым числом.\nВведите свой возраст, используя только цифры")


# ----------------------------------------- Check height. Age gotta be digit
@dp.message(lambda message: message.text.isdigit() and 90 <= int(message.text) <= 250, StateFilter(FSMFillForm.fill_height))
async def message_handler_height(message: types.Message, state: FSMContext):
    # Update state and data
    await state.set_state(FSMFillForm.fill_weight)
    height = int(message.text)
    msg = '4. Введи свой вес'
    await message.answer(text = msg, reply_markup=kb.do_not_answer)
    await state.update_data(height = height)
    print(await state.get_data())


@dp.message(StateFilter(FSMFillForm.fill_height))
async def message_handler_height_failed(message: types.Message, state: FSMContext):
    if message.text == "Не знаю/не хочу указывать":
        await message.reply("Хорошо. Рост можно не указывать или указать позже")
        await state.update_data(height = None)
        await state.set_state(FSMFillForm.fill_weight)
        await message.answer(text = '4. Введи свой вес', reply_markup=kb.do_not_answer)
    else:
        return await message.reply("Возраст должен быть целым числом.\nВведите свой возраст, используя только цифры")

# ----------------------------------------- Check weight. Age gotta be digit
@dp.message(StateFilter(FSMFillForm.fill_weight))
async def message_handler_weight(message: types.Message, state=FSMContext):
    if message.text == "Не знаю/не хочу указывать":
        await message.reply("Хорошо. Вес можно не указывать или указать позже")
        weight = None
    elif not message.text.isdigit():
        return await message.reply("Вес должен быть целым числом.\nВведите свой возраст, используя только цифры")
    else:
        weight = int(message.text)
    await state.update_data(weight = weight)
    markup = types.ReplyKeyboardRemove()
        # And send message
    data = await state.get_data() 
    await bot.send_message(message.chat.id, md.text(
                md.text(md.bold(data['name'], ', вот твои данные:')),
                md.text('Пол:', data['gender']),
                md.text('Возраст:', data['age']),
                md.text('Рост:', data['height']),
                md.text('Вес:', data['weight']),
                sep='\n'), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
            # Finish conversation
    print(data)
    await db.edit_user_db(message.from_user.id, data)
    state.clear
    await message.answer("Хотите пройти диагностику?", reply_markup=kb.answers_yes_no)
    await state.set_state(FSMFillForm.fill_diagnostics0)
   
@dp.callback_query(StateFilter(FSMFillForm.fill_diagnostics0))
async def callback_handler_diagnose0(callback_query: types.CallbackQuery, state: FSMContext):
    #await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    if callback_query.data == 'yes':
        await bot.send_message(callback_query.from_user.id, diagnostics.prompt1)
        await state.update_data(answers = 0)
        await state.update_data(cur_question = 1)
        text = diagnostics.questions1[0]
        await bot.send_message(callback_query.from_user.id, text, 
                                   reply_markup=kb.answers_diagnostics)
        await state.set_state(FSMFillForm.fill_diagnostics1)
    else:
        await state.set_state(FSMFillForm.show_menu)
        await bot.send_message(callback_query.from_user.id, 'Меню', 
                                   reply_markup=kb.actions)

# тут должны обрабатываться ответы
@dp.callback_query(StateFilter(FSMFillForm.fill_diagnostics1))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    # добавляем ответ в массив
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    data = await state.get_data()
    answers = data['answers'] + int(callback_query.data)
    await state.update_data(answers = answers)
    qs = diagnostics.questions1
        # ну и выводим некст вопрос
    if data['cur_question'] == len(qs):
            # а также в зависимости как вы работаете с стейтом делате или 
            #await state.finish()
            # или удаляете переменные в стейт ручками по типу
            #del data['answers']  
            await bot.send_message(callback_query.from_user.id, diagnostics.prompt2)
            await state.update_data(answers2 = 0)
            await state.update_data(cur_question = 1)
            text = diagnostics.questions2[0]
            await bot.send_message(callback_query.from_user.id, text, 
                                   reply_markup=kb.answers_yes_no)
            await state.set_state(FSMFillForm.fill_diagnostics2)
    else:
            text = qs[data['cur_question']]
            cur_question = data['cur_question'] + 1
            await state.update_data(cur_question = cur_question)
            await bot.send_message(callback_query.from_user.id, text, 
                                    reply_markup=kb.answers_diagnostics)

@dp.callback_query(StateFilter(FSMFillForm.fill_diagnostics2))
async def callback_handler_diagnose1(callback_query: types.CallbackQuery, state: FSMContext):
    # добавляем ответ в массив
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id)
    data = await state.get_data()
    if callback_query.data == 'yes':
        answers2 = data['answers2'] + 1
        await state.update_data(answers2 = answers2)
    qs = diagnostics.questions2
        # ну и выводим некст вопрос
    if data['cur_question'] == len(qs):
            text = 'Баллы за первую часть: ' + str(data['answers'])
            text += '\nБаллы за вторую часть: '
            text += str(answers2)
            text += '\n*ваш диагноз - лох, объелся блох*'
            prev_answers = db.get_user_db_score(callback_query.from_user.id)
            await db.edit_user_db_score(callback_query.from_user.id, data['answers'], answers2)
            if None in prev_answers:
                await bot.send_message(callback_query.from_user.id, text)
                await bot.send_message(callback_query.from_user.id, text_phrases.after_first_diagnostic, 
                                   reply_markup=kb.after_diagnosis)
                await state.set_state(FSMsetup.setup_functions0)
            else:
                await state.set_state(FSMFillForm.show_menu)
                await bot.send_message(callback_query.from_user.id, text + str(answers2), 
                                   reply_markup=kb.actions)
    else:
            text = qs[data['cur_question']]
            cur_question = data['cur_question'] + 1
            await state.update_data(cur_question = cur_question)
            await bot.send_message(callback_query.from_user.id, text, 
                                    reply_markup=kb.answers_yes_no)


@dp.message(Command('fillform'))
@dp.message(F.text =='💁‍♀️ Изменить информацию о себе', StateFilter(FSMFillForm.show_menu))
async def message_handler_change_info(message: types.Message, state: FSMContext):
    await message.delete()
    name, gender, age, height, weight = db.get_user_db(message.from_user.id)

    markup = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, md.text(
                md.text(md.bold(name, ', вот твои данные:')),
                md.text('Пол:', gender),
                md.text('Возраст:', age),
                md.text('Рост:', height),
                md.text('Вес:', weight),
                sep='\n'), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    await message.answer(text = 'Вы действительно хотите поменять информацию о себе?', reply_markup=kb.answers_yes_no)
    await state.set_state(FSMFillForm.fill_form)

@dp.callback_query(StateFilter(FSMFillForm.fill_form))
async def callback_handler_fill_form(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes':
        await bot.send_message(callback_query.from_user.id, '1. Выбери свой пол', reply_markup=kb.gender)
        await state.set_state(FSMFillForm.fill_gender)
    else:
        await bot.send_message(callback_query.from_user.id, 'Информация о Вас осталась прежней', 
                               reply_markup=kb.actions)
        await state.set_state(FSMFillForm.show_menu)
    
