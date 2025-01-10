from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
import os

async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Далее', callback_data='button1')
    keyboard.add(button)
    question = 'RM or Bacelona'
    answer = ['RM', 'Bacelona', 'Both']

    await bot.send_poll(
        chat_id=message.chat.id,    #куда отправляем
        question=question,          #вопрос
        options=answer,             #варианты ответов
        is_anonymous=0,             #анонимность
        type='quiz',                #тип отпроса: опрос или викторина
        correct_option_id=2,        #id правильного ответа
        explanation='Shame',        #подсказка
        open_period=60,             #время вывода опроса
        reply_markup=keyboard       #вывод кнопки под опросником
    )

async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Далее', callback_data='button2')
    keyboard.add(button)
    question = 'Dota2 or CS2'
    answer = ['Dota2', 'CS2', 'Both']
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=1,
        type='quiz',
        correct_option_id=1,
        explanation='Эх ты',
        open_period=60,
        reply_markup = keyboard
    )

async def quiz_3(call: types.CallbackQuery):
    question = 'Как называется это здание?'
    answer = ['Нотр-Дам-де-Пари', 'Кельнский собор']
    photo_path =  os.path.join('media', 'image1.jpg')
    photo = open(photo_path, 'rb')
    await bot.send_photo(chat_id=call.from_user.id,
                         photo=photo)
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=0,
        type='quiz',
        correct_option_id=0,
        explanation='Второе название: Собор Парижской Богоматери',
        open_period=60
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='button1')
    dp.register_callback_query_handler(quiz_3, text='button2')
