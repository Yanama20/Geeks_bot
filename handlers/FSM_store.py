from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import main_db


class FSM_store(StatesGroup):
    name_product = State()
    size = State()
    category = State()
    price = State()
    productid = State()
    infoproduct = State()
    collection = State()
    photo = State()
    submit = State()


async def start_fsm_store(message: types.Message):
    await FSM_store.name_product.set()
    await message.answer('Напишите название товара:')


async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await FSM_store.next()
    await message.answer('Выберете размер товара:', reply_markup = buttons.size)



async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await FSM_store.next()
    await message.answer('Напишите категорию продукта:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await FSM_store.next()
    await message.answer('Напишите стоимость товара:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await FSM_store.next()
    await message.answer('Напишите артикул товара:')


async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text

    await FSM_store.next()
    await message.answer('Напишите описание товара:')


async def load_infoproduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text

    await FSM_store.next()
    await message.answer('Напишите коллекцию товара:')


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await FSM_store.next()
    await message.answer('Отправьте фотографию товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await FSM_store.next()
        await message.answer('Верные ли данные ?')
        await message.answer_photo(photo=data['photo'],
                                   caption=f'Название товара - {data["name_product"]}\n'
                                    f'Размер - {data["size"]}\n'
                                    f'Категория - {data["category"]}\n'
                                    f'Стоимость - {data["price"]}\n'
                                    f'Артикул - {data["productid"]}\n'
                                    f'Коллекция - {data["collection"]}\n'
                                    f'Описание товара - {data["infoproduct"]}', reply_markup=buttons.submit)



async def submit(message: types.Message, state: FSMContext):
    if message.text == 'да':
        async with state.proxy() as data:
            await main_db.sql_insert_store(
                name_product=data['name_product'],
                size=data['size'],
                price=data['price'],
                productid=data['productid'],
                photo=data['photo'],
            )
            await main_db.sql_insert_product_details(
                category=data['category'],
                productid=data['productid'],
                infoproduct=data['infoproduct'],
            )
            await main_db.sql_insert_collection(
                productid=data['productid'],
                collection=data['collection'],
            )
            await message.answer('Ваши данные в базе', reply_markup=buttons.remove_keyboard)

        await state.finish()

    elif message.text == 'нет':
        await message.answer('Хорошо, отменено!', reply_markup=buttons.remove_keyboard)
        await state.finish()

    else:
        await message.answer('Выберите да или нет')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.remove_keyboard)


def register_handlers_fsm_reg(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm_store, commands='product_registration')
    dp.register_message_handler(load_name_product, state=FSM_store.name_product)
    dp.register_message_handler(load_size, state=FSM_store.size)
    dp.register_message_handler(load_category, state=FSM_store.category)
    dp.register_message_handler(load_price, state=FSM_store.price)
    dp.register_message_handler(load_productid, state=FSM_store.productid)
    dp.register_message_handler(load_infoproduct, state=FSM_store.infoproduct)
    dp.register_message_handler(load_collection, state=FSM_store.collection)
    dp.register_message_handler(load_photo, state=FSM_store.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_store.submit)