from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    waiting_name = State()


class AddFood(StatesGroup):
    waiting_name = State()
    waiting_image = State()
    waiting_recipe = State()


class EditFood(StatesGroup):
    waiting_new_name = State()
    waiting_new_image = State()
    waiting_new_recipe = State()


class SearchFood(StatesGroup):
    waiting_query = State()
