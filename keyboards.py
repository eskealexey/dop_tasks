from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Стартовая клавиатура
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список задач"),
            KeyboardButton(text="Информация"),
        ],
        [
            KeyboardButton(text="Добавить задачу"),
        ]
    ], resize_keyboard=True
)

# рабочая клавиатура
work_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Редактировать", callback_data='edit'),
            InlineKeyboardButton(text="Удалить", callback_data='delete'),
        ]
    ]
)
