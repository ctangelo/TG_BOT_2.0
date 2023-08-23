from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from dispatcher import bot, dp
from keyboard.admin_kb import currency_btn, gen_inline_exchange_orders, gen_inline_main_menu, gen_inline_consultant_orders
from keyboard.client_kb import review_btn
from database import sqlite_db


ID = 245955512

class FSMAddcurrency(StatesGroup):
    rub = State()
    kzt = State()
    kgs = State()
    uzs = State()
    usdt = State()


# @dp.callback_query_handler(commands=['admin_menu'])
async def admin_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Здравствуйте, вот список заявок', reply_markup=gen_inline_main_menu())

# @dp.callback_query_handler(text='add_currency')
async def currency_order(callback: types.CallbackQuery):
    # if callback.message.from_user.id == ID:
    await callback.message.answer('Добавим новый курс валют?', reply_markup=currency_btn)


# @dp.callback_query_handler(text='currency_yes', state=None)
async def currency_start(callback: types.CallbackQuery):
    
    await FSMAddcurrency.rub.set()
    await callback.message.answer('Сколько VND за 10.000 RUB?')


# @dp.message_handler(state=FSMAddcurrency.rub)
async def rub_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rub'] = int(message.text) / 10000
    await FSMAddcurrency.next()
    await message.answer('Сколько VND за 10.000 KZT?')


# @dp.message_handler(state=FSMAddcurrency.kzt)
async def kzt_load(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        data['kzt'] = int(message.text) / 10000
    await FSMAddcurrency.next()
    await message.answer('Сколько VND за 1.000 KGS?')


# @dp.message_handler(state=FSMAddcurrency.kgs)
async def kgs_load(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['kgs'] = int(message.text) / 1000
    await FSMAddcurrency.next()
    await message.answer('Сколько VND за 100.000 UZS?')


# @dp.message_handler(state=FSMAddcurrency.uzs)
async def uzs_load(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['uzs'] = int(message.text) / 10000
    await FSMAddcurrency.next()
    await message.answer('Сколько VND за 1 USDT?')


# @dp.message_handler(state=FSMAddcurrency.usdt)
async def usdt_load(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['usdt'] = int(message.text)
    await sqlite_db.add_currency(state)
    await message.answer('Готово')
    await state.finish()
    

# @dp.callback_query_handler(commands='consultant_order')
async def consultant_order(callback: types.CallbackQuery):
    await callback.message.delete()
    data = await sqlite_db.all_consultant()
    await callback.message.answer('Заявки на консультацию', reply_markup=gen_inline_consultant_orders(data))


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('one_consultant|'))
async def consultant_one_order(callback: types.CallbackQuery):
    await callback.message.delete()
    order = await sqlite_db.one_consultant(callback.data.split('|')[1])
    chat_id = callback.data.split('|')[1]
    button_url = f'tg://user?id={chat_id}'
    markup = InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='написать пользователю', url=button_url))
    markup.add(InlineKeyboardButton(text='Заявка исполнена', callback_data=f'ready|consultant|{order[0]}'))
    markup.add(InlineKeyboardButton(text='Удалить заявку', callback_data=f'delete|consultant|{order[0]}'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='consultant_order'))
    await bot.send_message(ID, f'Заявка на консультацию {order[0]}', reply_markup=markup)

   

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete|'))
async def delete_order(callback: types.CallbackQuery):
    # await callback.message.delete()
    data = callback.data.split('|')

    if data[1] == 'exchange':
        await sqlite_db.delete_exchange(data[2], data[3])
        await exchange_order(callback)

    elif data[1] == 'consultant':
        await sqlite_db.delete_consultant(data[2])
        await consultant_order(callback)


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('ready|'))
async def ready_order(callback: types.CallbackQuery):
    data = callback.data.split('|')

    if data[1] == 'exchange':
        await sqlite_db.delete_exchange(data[2], data[3])
        await exchange_order(callback)
        await bot.send_message(data[2], 'Спасибо что воспользовались нашими услугами по обмену валюты!', reply_markup=review_btn)

    elif data[1] == 'consultant':
        await sqlite_db.delete_consultant(data[2])
        await consultant_order(callback)
        await bot.send_message(data[2], 'Спасибо что воспользовались нашими услугами по обмену валюты!', reply_markup=review_btn)


# @dp.callback_query_handler(text='exchange_order')
async def exchange_order(callback: types.CallbackQuery):
    await callback.message.delete()
    data = await sqlite_db.see_exchange()
    await callback.message.answer('Заявки на обмен', reply_markup=gen_inline_exchange_orders(data))


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('one_exchange|'))
async def exchange_one_order(callback: types.CallbackQuery):
    await callback.message.delete()
    order = await sqlite_db.one_exchange(callback.data.split('|')[1], callback.data.split('|')[2])
    chat_id = callback.data.split('|')[1]
    button_url = f'tg://user?id={chat_id}'
    markup = InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='написать пользователю', url=button_url))
    markup.add(InlineKeyboardButton(text='Заявка исполнена', callback_data=f'ready|exchange|{order[0]}|{order[3]}'))
    markup.add(InlineKeyboardButton(text='Удалить заявку', callback_data=f'delete|exchange|{order[0]}|{order[3]}'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='exchange_order'))
    
    await callback.message.answer(f'Обмен\n{order[3]} {order[1]} на {order[4]} VND\nБанк: {order[2]}', reply_markup=markup)


def register_admin_handler(dp: Dispatcher):
    dp.register_callback_query_handler(currency_order, text='add_currency')
    dp.register_callback_query_handler(currency_start, text='currency_yes', state=None)
    dp.register_message_handler(rub_load, state=FSMAddcurrency.rub)
    dp.register_message_handler(kzt_load, state=FSMAddcurrency.kzt)
    dp.register_message_handler(kgs_load, state=FSMAddcurrency.kgs)
    dp.register_message_handler(uzs_load, state=FSMAddcurrency.uzs)
    dp.register_message_handler(usdt_load, state=FSMAddcurrency.usdt)


    dp.register_callback_query_handler(admin_menu, text='admin_menu')

    dp.register_callback_query_handler(consultant_order, text='consultant_order')
    dp.register_callback_query_handler(consultant_one_order, lambda x: x.data and x.data.startswith('one_consultant|'))

    dp.register_callback_query_handler(delete_order, lambda x: x.data and x.data.startswith('delete|')) 
    dp.register_callback_query_handler(ready_order, lambda x: x.data and x.data.startswith('ready|')) 

    dp.register_callback_query_handler(exchange_order, text='exchange_order')
    dp.register_callback_query_handler(exchange_one_order, lambda x: x.data and x.data.startswith('one_exchange|'))