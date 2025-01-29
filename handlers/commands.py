from aiogram import Dispatcher, types
from config import bot
import os
from random import choice

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}!\n'
                                f'Твой telegram ID - {message.from_user.id}\n')
    # await message.answer('Привет!')


async def mem_handler(message: types.Message):
    photo_path = os.path.join('media', 'images.jpg')
    photo = open(photo_path, 'rb')

    await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo,
                             caption='Это мем')

    # with open(photo_path, 'rb') as photo:
    #     await bot.send_photo(chat_id=message.from_user.id,
    #                          photo=photo,
    #                          caption='Это мем')
    # await message.answer_photo(photo=photo, caption='Мем')


async def sqr_handler(message: types.Message):
    if int(message.text):
        num = int(message.text)
        sqr = num ** 2
        await bot.send_message(chat_id=message.from_user.id,
                             text=f'Квадрат вашего числа = {sqr}\n')
dice_options = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
async def game_dice(message: types.Message):
    random_dice = choice(dice_options)

    bot_message = await bot.send_dice(chat_id=message.from_user.id,emoji=random_dice)
    bot_score = bot_message.dice.value
    print(bot_score)

    user_message = await bot.send_dice(chat_id=message.from_user.id, emoji=random_dice)
    user_score = user_message.dice.value
    print(user_score)

    if bot_score > user_score:
        await message.answer('Вы проиграли!')
    elif bot_score < user_score:
        await message.answer('Вы выйграли!')
    elif bot_score == user_score:
        await message.answer('Ничья!')


    # await bot.send_dice(chat_id=message.from_user.id,
    #                     emoji='🏀')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands='start')
    dp.register_message_handler(mem_handler, commands='mem')
    dp.register_message_handler(sqr_handler, commands='sqr')
    dp.register_message_handler(game_dice, commands='game')
