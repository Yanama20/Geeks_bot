from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


start = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton('/start'),
    KeyboardButton('/mem'),
    KeyboardButton('/quiz'),
    KeyboardButton('/reply_webapp'),
    KeyboardButton('/inline_webapp'),
    KeyboardButton('/product_registration'))

size = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(KeyboardButton('XS'),KeyboardButton('S'),KeyboardButton('M'),KeyboardButton('L'),KeyboardButton('XL'),KeyboardButton('XXL'),KeyboardButton('XXXL'),)
submit = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(KeyboardButton('да'), KeyboardButton('нет'))

remove_keyboard = ReplyKeyboardRemove()