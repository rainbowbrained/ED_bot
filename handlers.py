import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
import kb, text, diagnostics
import config
#from handlers import router

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

dp.callback_query_handler()
async def c_q(c: types.CallbackQuery):
    await print(c.data, c.message)
    await c.answer(text = '!!!'+c.data)
    #return await c.answer(text = '!!!'+c.data)
    #print(c.data, c.message)


@dp.message_handler(commands='test')
async def test_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker = 'CAACAgIAAxkBAAEJdrZklsegDfBEGrt5HkcxjpwonqCdnwAClxgAAi_k6EoUpiaOwK-a9S8E')


@dp.message_handler(commands='start')
async def help_command(message: types.Message):
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=kb.actions)
    await message.delete()
    await message.answer(text = '1. Выбери свой пол', reply_markup=kb.gender)
    await message.answer(text = '2. Введи свой возраст')
    await message.answer(text = '3. Введи свой рост')
    await message.answer(text = '4. Введи свой вес', reply_markup=kb.do_not_answer)



@dp.message_handler(commands='help')
async def start_command(message: types.Message):
    await message.reply(text=text.HELP_COMMAND, parse_mode='HTML')

@dp.message_handler(commands='diagnostics')
async def start_command(message: types.Message):
    for q in diagnostics.questions1:
        await message.answer(text = q, reply_markup=kb.answers1)
    for q in diagnostics.questions2:
        await message.answer(text = q, reply_markup=kb.answers2)
    
'''
@dp.callback_query_handler(text = 'log_food')
async def process_callback_button23(c_q: types.CallbackQuery):
    print('!!!')
    await c_q.message.answer(text = 'Класс! Расскажи подробнее, что ты съел', reply_markup=kb.log_food)
    await c_q.message.delete()

@dp.message_handler(regexp='🥦 Поел')
async def start_command(message: types.Message):
    await message.answer(text = '!', reply_markup=kb.log_food)
    
''' 

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Твой ID: {message.from_user.id}")
    

@dp.message(F.text == "Меню")
@dp.message(F.text == "Выйти в меню")
@dp.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

'''
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

'''

if __name__ == "__main__":
    executor.start_polling(dp)
