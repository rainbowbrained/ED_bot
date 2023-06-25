'''
все клавиатуры бота, статические и динамические
'''
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo

menu = [
    [InlineKeyboardButton(text="📝 Пройти тест", callback_data="start_diagnostics"),
    InlineKeyboardButton(text="🖼 Генерировать изображение", callback_data="generate_image")],
    [InlineKeyboardButton(text="💳 Купить токены", callback_data="buy_tokens"),
    InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
    [InlineKeyboardButton(text="💎 Партнёрская программа", callback_data="ref"),
    InlineKeyboardButton(text="🎁 Бесплатные токены", callback_data="free_tokens")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
#-------------------------------------------------------------
gender = [
    [InlineKeyboardButton(text="🙍‍♂️ Мужской", callback_data="man")],
    [InlineKeyboardButton(text="🙍‍♀️ Женский", callback_data="woman")],
    [InlineKeyboardButton(text="🥷 Другое", callback_data="other")]
]
gender = InlineKeyboardMarkup(inline_keyboard=gender)
do_not_answer = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Не знаю/не хочу указывать", callback_data="no_weight")]], resize_keyboard=True, one_time_keyboard=True)
#-------------------------------------------------------------

answers1 = [
    [InlineKeyboardButton(text="Никогда", callback_data="0")],
    [InlineKeyboardButton(text="Редко", callback_data="0")],
    [InlineKeyboardButton(text="Иногда", callback_data="0")],
    [InlineKeyboardButton(text="Часто", callback_data="1")],
    [InlineKeyboardButton(text='Как правило', callback_data="2")],
    [InlineKeyboardButton(text="Постоянно", callback_data="3")]
]
answers1 = InlineKeyboardMarkup(inline_keyboard=answers1, resize_keyboard=True)
#-------------------------------------------------------------

answers2 = [
    [InlineKeyboardButton(text="Нет", callback_data="0")],
    [InlineKeyboardButton(text="Да", callback_data="1")],
]
answers2 = InlineKeyboardMarkup(inline_keyboard=answers2, resize_keyboard=True)

#-------------------------------------------------------------web_app=WebAppInfo('https://rainbowbrained.github.io/ED_bot/'),
actions = [
    [KeyboardButton(text="💧 Попил воды", callback_data="log_water"),
     KeyboardButton(text="🥦 Поел",  web_app=WebAppInfo(url = 'https://rainbowbrained.github.io/ED_bot/'), callback_data="log_food")],
    [KeyboardButton(text="😟 Хочу сорваться", callback_data="0"),
     KeyboardButton(text="😨 Сорвался", callback_data="1")],
    [KeyboardButton(text="📈 Показать трекеры", callback_data="1")],
    [KeyboardButton(text='💁‍♀️ Изменить информацию о себе', callback_data="change_information")]
]
actions = ReplyKeyboardMarkup(keyboard=actions, resize_keyboard=True, one_time_keyboard=True)
#-------------------------------------------------------------

log_food = [
    [KeyboardButton(text="🍳 Завтрак", callback_data="log_breakfast"),
     KeyboardButton(text="🍝 Обед", callback_data="log_lunch")],
    [KeyboardButton(text="🍗 Ужин", callback_data="log_dinner"),
     KeyboardButton(text="🍏 Перекус", callback_data="log_snack")],
    [KeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]
log_food = ReplyKeyboardMarkup(keyboard=log_food, resize_keyboard=True, one_time_keyboard=True)
