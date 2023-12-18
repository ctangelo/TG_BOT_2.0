from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from dispatcher import bot, dp
from keyboard.client_kb import inline_menu, choose_bank_btn, back_btn
from keyboard.client_kb import exchange_btn, currency_btn, approve_btn
from keyboard.admin_kb import gen_inline_main_menu
from handlers.admin import ID
from database import sqlite_db
import math
from datetime import datetime


# @dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    photo = open("/root/TG_BOT_2.0/photo/logo3.png", 'rb')
    await bot.send_photo(message.from_user.id, photo, caption='👋Привет! Добро пожаловать в Тур Обмен - валютно обменный чат-бот. Я здесь, чтобы помочь вам с информацией о текущих обменных курсах и провести операции по обмену валюты. Если у вас есть какие-либо вопросы, не стесняйтесь спрашивать. Начнем! /menu')


# @dp.message_handler(commands=['menu'], state="*")
async def menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:  
        await state.finish()
    
    if message.from_user.id == ID:
        await message.answer('Здравствуйте, вот список заявок', reply_markup=gen_inline_main_menu())
    else:
        await message.answer('Чем я могу Вам помочь сегодня?', reply_markup=inline_menu)


# @dp.callback_query_handler(text=['menu'])
async def menu_2(callback: types.CallbackQuery):
    await callback.message.delete()
    
    await callback.message.answer('Чем я могу Вам помочь сегодня?', reply_markup=inline_menu)

# @dp.message_handler(commands=['consultant'], state="*")
async def consultant(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:  
        await state.finish()
    await message.delete()
    await message.answer('Ваша заявки принята, консультант свяжется с вами в ближайшее время', reply_markup=back_btn)
    check_user = await sqlite_db.one_consultant(message.from_user.id)
    print(check_user)
    if check_user[0] == message.from_user.id:
        print(check_user)
    else:
        await sqlite_db.add_consultant(message.from_user.id)
        print(check_user)
    

# @dp.callback_query_handler(text=['consultant'])
async def consultant_2(callback: types.CallbackQuery):
    await callback.message.answer('Ваша заявки принята, консультант свяжется с вами в ближайшее время', reply_markup=back_btn)
    await callback.message.delete()
    await sqlite_db.add_consultant(callback.from_user.id)
    

# @dp.callback_query_handler(text=['how_it_works'])
async def how_it_works(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('🔹 Выбор валюты: Выберите валюту, которую хотите обменять.\n\n'
                                  '🔹 Укажите сумму: Выберите сумму для обмена. \n\n'
                                  '🔹 Получите выгодный курс: Мы предоставим Вам лучший доступный курс обмена. \n\n'
                                  '🔹 Подтвердите операцию: Фиксируем курс, одобрите операцию обмена и внесите свои данные. \n\n'
                                  '🔹 Получите вторую валюту: Наш курьер доставит VND (Вьетнамский донг), после чего Вы переведете свою валюту по зафиксированному курсу.'
                                  '🔹 График работы: Ежедневно с 09:00 до 18:00', reply_markup=back_btn)

# @dp.callback_query_handler(text=['advantages'])
async def advantages(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('🔹 Обширное покрытие: принимаем к онлайн обмену: RUB (Российский рубль), KZT (Казахстанский тенге), KGS (Кыргызский сом), UZS (Узбекский сум), USDT (Tether)\n\n' 
                                  '🔹 Лучшие курсы: получите самые выгодные курсы на рынке. \n\n'
                                  '🔹 Быстро и удобно: Совершайте операции обмена за несколько кликов. Быстрая доставка VND (Вьетнамский донг) до двери. \n\n'
                                  '🔹 Прозрачность: Ознакомьтесь с актуальными курсами перед проведением операции.', reply_markup=back_btn)



# __________________Калькулятор__________________________

class FSMCalculator(StatesGroup):
    currency = State()
    amount = State()


# @dp.callback_query_handler(text=['calculator'], state=None)
async def calculator(callback: types.CallbackQuery):
    await FSMCalculator.currency.set()
    await callback.message.delete()
    await callback.message.answer('Какую валюту хотите продать?', reply_markup=currency_btn)
    
# @dp.callback_query_handler(state=FSMCalculator.currency)
async def load_currency(callback: types.CallbackQuery, state=FSMContext):
     async with state.proxy() as data:
         data['currency'] = callback.data
     await FSMCalculator.next()
     await callback.message.delete()
     await callback.message.answer('Введите сумму:')


# @dp.message_handler(state=FSMExchange.amount)
async def load_amount(message: types.Message, state=FSMContext):
    try:
        amount = message.text
        async with state.proxy() as data:
            data['amount'] = amount
            
            rate = sqlite_db.check_currency(data['currency'])
            sum = rate * int(amount)
            
            data['vnd_amount'] = math.floor(sum)
            
        await message.delete()
        await message.answer(f'Вы получите {"{0:,}".format(int(math.floor(sum))).replace(",", " ")} VND', reply_markup=back_btn)
        await state.finish()
        

    except ValueError:
        await FSMCalculator.amount.set()
        await message.answer('Введите число цифрами:')

# __________________Обмен денег _________________________


class FSMExchange(StatesGroup):
    currency = State()
    bank = State()
    amount = State()
    aprove = State()
    

# @dp.callback_query_handler(text=['exchange'], state=None)
async def exchange_start(callback: types.CallbackQuery):
     await FSMExchange.currency.set()
     await callback.message.delete()
     await callback.message.answer('Какую валюту хотите продать?', reply_markup=currency_btn)


# @dp.callback_query_handler(state=FSMExchange.currency)
async def currency_load(callback: types.CallbackQuery, state=FSMContext):
     async with state.proxy() as data:
         data['user_id'] = callback.from_user.id
         data['currency'] = callback.data
     await FSMExchange.next()
     await callback.message.delete()

     if data['currency'] == 'usdt':
        async with state.proxy() as data:
            data['bank'] = 'none'
        await FSMExchange.next()
        await callback.message.answer('Введите сумму:')

     else:
        await callback.message.answer('Какой банк?', reply_markup=choose_bank_btn(data['currency']))


# @dp.callback_query_handler(state=FSMExchange.city)
async def bank_load(callback: types.CallbackQuery, state=FSMContext):
     async with state.proxy() as data:
         data['bank'] = callback.data
     await FSMExchange.next()
     await callback.message.delete()
     
     await callback.message.answer('Введите сумму:')
     

# @dp.message_handler(state=FSMExchange.amount)
async def amount_load(message: types.Message, state=FSMContext):
    try:
        amount = message.text
        async with state.proxy() as data:
            data['amount'] = amount
            rate = sqlite_db.check_currency(data['currency'])
            sum = rate * int(amount)
            data['vnd_amount'] = math.floor(sum)
            
        await FSMExchange.next()
        await message.delete()
        await message.answer(f'Вы получите {"{0:,}".format(int(math.floor(sum))).replace(",", " ")} VND', reply_markup=approve_btn)
    except ValueError:
        await FSMExchange.amount.set()
        await message.answer('Введите число цифрами:')
        


# @dp.callback_query_handler(state=FSMExchange.approve)
async def approve_exchange(callback: types.CallbackQuery, state=FSMContext):
    if callback.data == 'aprove':
        async with state.proxy() as data:
            data['aprove'] = 'yes'
            data['time'] = datetime.now()
            amount = int(data['amount'])
            
            currency = data['currency']
            vnd_amount = data['vnd_amount']
        await sqlite_db.add_exchange(state)
        await state.finish()
        await callback.message.delete()
        await callback.message.answer(f'Обмен {"{0:,}".format(amount).replace(",", " ")} {currency} на {"{0:,}".format(vnd_amount).replace(",", " ")} VND\n Спасибо, ваша заявка принята, оператор свяжется с вами в ближайшее время', reply_markup=back_btn)
        

    else:
        await state.finish()
        await callback.message.delete()
        await menu_2(callback)

# __________________Отзывы _________________________

class FSMReview(StatesGroup):
    review = State()
    
# @dp.callback_query_handler(text=['review'], state=None)
async def review_start(callback: types.CallbackQuery):
     await FSMReview.review.set()
     await callback.message.delete()
     await callback.message.answer('Напишите свой отзыв:')


# @dp.message_handler(state=FSMReview.review)
async def review_load(message: types.Message, state=FSMContext):
    await bot.forward_message(-1001834865804, message.from_user.id, message.message_id)
    await state.finish()
    await message.answer('Спасибо, за отзыв')

# __________________Курс Валют _________________________


# @dp.callback_query_handler(text=['course'])
async def course(callback: types.CallbackQuery):
    await callback.message.delete()
    usdt = int(sqlite_db.check_currency('usdt') * 100)
    rub = int(sqlite_db.check_currency('rub') * 10000)
    kzt = int(sqlite_db.check_currency('kzt') * 50000)
    kgs = int(sqlite_db.check_currency('kgs') * 10000)
    uzs = int(sqlite_db.check_currency('uzs') * 1000000)

    await callback.message.answer(f'🇺🇸 100 USDT = {"{0:,}".format(usdt).replace(",", " ")} VND\n🇷🇺 10 000 RUB = {"{0:,}".format(rub).replace(",", " ")} VND\n'
                         f'🇰🇿 50 000 KZT = {"{0:,}".format(kzt).replace(",", " ")} VND\n🇰🇬 10 000 KGS = {"{0:,}".format(kgs).replace(",", " ")} VND\n'
                         f'🇺🇿 1 000 000 UZS = {"{0:,}".format(uzs).replace(",", " ")} VND', reply_markup=back_btn)


# __________________Регистрация хендлеров _________________________

def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start'])
    dp.register_message_handler(menu, commands=['menu'], state="*")
    dp.register_callback_query_handler(menu_2, text=['main_menu'])

    dp.register_message_handler(consultant, commands=['consultant'], state="*")
    dp.register_callback_query_handler(consultant_2, text=['consultant'])

    dp.register_callback_query_handler(advantages, text=['advantages'])
    dp.register_callback_query_handler(how_it_works, text=['how_it_works'])

    dp.register_callback_query_handler(calculator, text=['calculator'], state=None)
    dp.register_callback_query_handler(load_currency, state=FSMCalculator.currency)
    dp.register_message_handler(load_amount, state=FSMCalculator.amount)
    
    dp.register_callback_query_handler(exchange_start, text=['exchange'], state=None)
    dp.register_callback_query_handler(currency_load, state=FSMExchange.currency)
    dp.register_callback_query_handler(bank_load, state=FSMExchange.bank)
    dp.register_message_handler(amount_load, state=FSMExchange.amount)
    dp.register_callback_query_handler(approve_exchange, state=FSMExchange.aprove)
    
    dp.register_callback_query_handler(review_start, text=['review'], state=None)
    dp.register_message_handler(review_load, state=FSMReview.review)

    dp.register_callback_query_handler(course, text=['course'])