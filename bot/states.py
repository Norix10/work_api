from aiogram.fsm.state import State, StatesGroup


class FilterStates(StatesGroup):
    waiting_technologies = State()
    waiting_level = State()
    waiting_remote = State()
    waiting_salary = State()


LEVEL_MAP = {
    "Junior": "junior",
    "Middle": "middle",
    "Senior": "senior",
    "Любий рівень": "any",
}

REMOTE_MAP = {
    "Повністю віддалений": "full_remote",
    "Офісний": "office",
    "Частково віддалений": "part_time",
    "Любий формат": "any",
}
