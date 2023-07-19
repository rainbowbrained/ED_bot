'''
будет хранить вспомогательные классы для FSM (машины состояний), 
также фабрики Callback Data для кнопок Inline клавиатур
'''  

from aiogram.fsm.state import State, StatesGroup, default_state

class FSMFillForm(StatesGroup):
    fill_form = State()
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола _
    fill_height = State()
    fill_weight = State()
    fill_end = State()

    fill_diagnostics0 = State()
    fill_diagnostics1 = State()
    fill_diagnostics2 = State()
    show_menu = State()

class FSMsetup(StatesGroup):
    setup_functions0 = State()
    setup_functions_water = State()
    setup_functions_water_reminder = State()
    setup_functions_sleep = State()
    setup_functions_sleep_reminder = State()

class FSMRedButton(StatesGroup):
    action_state = State()
    feeling_state = State()
    intencity_state = State()
    reminder_state = State()
    better_state = State()
    post_better_state = State()
    practice_state = State()
    ending_state = State()

