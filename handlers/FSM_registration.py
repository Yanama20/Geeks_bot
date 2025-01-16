from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

# название товара, размер, категория, стоимость и фото товара.
class FSM_store(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    submit = State()


async def start_fsm_store(message: types.Message):
    await FSM_store.product_name.set()
    await message.answer('Напишите название товара:')


async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text

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
    await message.answer('Отправьте фотографию товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await FSM_store.next()
        await message.answer('Верные ли данные ?')
        await message.answer_photo(photo=data['photo'],
                                   caption=f'Название товара - {data["product_name"]}\n'
                                    f'Размер - {data["size"]}\n'
                                    f'Категория - {data["category"]}\n'
                                    f'Стоимость - {data["price"]}\n', reply_markup=buttons.submit)

async def submit(message: types.Message, state: FSMContext):
    if message.text == 'да':
        await message.answer('Ваши данные в базе', reply_markup=buttons.remove_keyboard)
        await state.finish()
        # Запись в базу

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
    dp.register_message_handler(load_product_name, state=FSM_store.product_name)
    dp.register_message_handler(load_size, state=FSM_store.size)
    dp.register_message_handler(load_category, state=FSM_store.category)
    dp.register_message_handler(load_price, state=FSM_store.price)
    dp.register_message_handler(load_photo, state=FSM_store.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_store.submit)