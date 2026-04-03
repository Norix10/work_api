from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎛 Мої фільтри"), KeyboardButton(text="💼 Вакансії")],
        [KeyboardButton(text="⚙️ Налаштування "), KeyboardButton(text="🛑 Стоп")],
    ],
    resize_keyboard=True
)


filters_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Створити"), KeyboardButton(text="✏️ Оновити")],
        [KeyboardButton(text="🗑 Видалити"), KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

level_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Junior"), KeyboardButton(text="Middle")],
        [KeyboardButton(text="Senior"), KeyboardButton(text="Любий рівень")],
    ],
    resize_keyboard=True
)

remote_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Повністю віддалений"), KeyboardButton(text="Офісний")],
        [KeyboardButton(text="Частково віддалений"), KeyboardButton(text="Любий формат")],
    ],
    resize_keyboard=True
)

