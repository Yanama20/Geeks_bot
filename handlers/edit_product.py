from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import main_db

class EditProduct(StatesGroup):
    for_field = State()
    for_new_photo = State()
    for_new_value = State()

async def start_edit_product(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    buntton_all = InlineKeyboardButton('Вывести все товары', callback_data='edit_all_products')
    buntton_by_one = InlineKeyboardButton('Вывести товары по одному', callback_data='edit_by_one_products')
    keyboard.add(buntton_all, buntton_by_one)

    await message.answer('Выберите как просмотреть товары:' , reply_markup=keyboard)

async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название - {product["name_product"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Артикул - {product["productid"]}\n'
                       f'Информация о товаре - {product["infoproduct"]}\n'
                       f'Цена - {product["price"]}\n'
                       f'Коллекция - {product["collection"]}\n')
            edit_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            edit_button = types.InlineKeyboardButton('Edit',
                                                       callback_data=f'edit_{product["productid"]}')
            edit_keyboard.add(edit_button)

            await call.message.answer_photo(photo=product["photo"], caption=caption, reply_markup=edit_keyboard)

    else:
        await call.message.answer('База пуста! Товаров нет.')

async def edit_products(call: types.CallbackQuery, state: FSMContext):
    prodctid = call.data.split('_')[1]

    await state.update_data(productid=prodctid)
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    name_button = InlineKeyboardButton(text="Название", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Категория", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Цена", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Размер", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Фото", callback_data="field_photo")
    info_button = InlineKeyboardButton(text="Инфо о товаре", callback_data="field_infoproduct")
    collection_button = InlineKeyboardButton(text="Коллекция", callback_data="field_collection")
    keyboard.add(name_button, category_button, price_button, size_button, photo_button, info_button, collection_button)

    await call.message.answer('Выберите информацию для редактирования:', reply_markup=keyboard)

    await EditProduct.for_field.set()

async def select_field (call: types.CallbackQuery, state: FSMContext):
    field_map ={
        'field_name_product': 'name_product',
        'field_category': 'category',
        'field_price': 'price',
        'field_size': 'size',
        'field_photo': 'photo',
        'field_infoproduct': 'infoproduct',
        'field_collection': 'collection'
    }

    field = field_map.get(call.data)

    if not field:
        await call.message.answer('Недопустимое поле.')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await EditProduct.for_new_photo.set()
        await call.message.answer('Отправьте новое фото:')
    else:
        await EditProduct.for_new_value.set()
        await call.message.answer('Введите новое значение:')


async def load_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    productid = user_data['productid']
    field = user_data['field']

    new_value = message.text
    main_db.update_product_field(productid, field, new_value)
    await message.answer(f'Поле {field} успешно обновлена.\n'
                         'Обновите список.')
    await state.finish()

async def load_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    productid = user_data['productid']
    photo_id  = message.photo[-1].file_id

    main_db.update_product_field(productid, 'photo', photo_id)
    await message.answer('Фото успешно обновлена.\n'
                         'Обновите список.')
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_edit_product, commands=['edit_store'])
    dp.register_callback_query_handler(send_all_products, Text(equals=['edit_all_products']))
    dp.register_callback_query_handler(edit_products, Text(startswith=['edit_']), state='*')
    dp.register_callback_query_handler(select_field, Text(startswith=['field_']),
                                       state=EditProduct.for_field)
    dp.register_message_handler(load_new_value, state=EditProduct.for_new_value)
    dp.register_message_handler(load_new_photo, state=EditProduct.for_new_photo, content_types=['photo'])


