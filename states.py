from aiogram.dispatcher.filters.state import State, StatesGroup

class Mail(StatesGroup):
    photo = State()
    description = State()

class StartBomber(StatesGroup):
    number = State()
    iterations = State()

class GiveSub(StatesGroup):
    id = State()
    days = State()

class AddWhitelist(StatesGroup):
    number = State()

class TakeSub(StatesGroup):
    id = State()