from aiogram import types, Dispatcher

async def reply_webapp(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    youtube = types.KeyboardButton('Youtube', web_app=types.WebAppInfo(url='https://www.youtube.com'))
    geeks_online= types.KeyboardButton('Geeks Online', web_app=types.WebAppInfo(url='https://online.geeks.kg/'))

    keyboard.add(geeks_online, youtube)

    await message.answer(text='Reply buttons: ', reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(reply_webapp, commands=['reply_webapp'])