from aiogram import types, Dispatcher

async def reply_webapp(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    youtube = types.KeyboardButton('Youtube', web_app=types.WebAppInfo(url='https://www.youtube.com'))
    geeks_online= types.KeyboardButton('Geeks Online', web_app=types.WebAppInfo(url='https://online.geeks.kg/'))
    git_hub = types.KeyboardButton('Git Hub', web_app=types.WebAppInfo(url='https://github.com'))
    netflix = types.KeyboardButton('Netflix', web_app=types.WebAppInfo(url='https://www.netflix.com/'))

    keyboard.add(geeks_online, youtube, git_hub, netflix)

    await message.answer(text='Reply buttons: ', reply_markup=keyboard)

async def inline_webapp(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    spotify = types.InlineKeyboardButton(text='Spotify', url='https://www.spotify.com/')
    jutsu = types.InlineKeyboardButton(text='Jutsu', url='https://www.jut.su/')
    kinokrad = types.InlineKeyboardButton(text='Kinokrad', url='https://www.kinokrad.com/')
    oc_kg = types.InlineKeyboardButton(text='OC KG', url='https://oc.kg/')
    keyboard.add(spotify, jutsu, kinokrad, oc_kg)
    await message.answer(text='Inline buttons: ', reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(reply_webapp, commands=['reply_webapp'])
    dp.register_message_handler(inline_webapp, commands=['inline_webapp'])