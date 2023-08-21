from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dispatcher import bot
from database import sqlite_db


def gen_inline_main_menu():
    admin_btn = InlineKeyboardMarkup(row_width=1)
    exchange_btn = InlineKeyboardButton(f'Обмен валюты ({sqlite_db.count_exchange()})', callback_data='exchange_order')
    currency_btn = InlineKeyboardButton('Добавить курс валют', callback_data='add_currency')
    consultant_btn = InlineKeyboardButton(f'Консультации ({sqlite_db.count_consultant()[0]})', callback_data='consultant_order')
    admin_btn.add(exchange_btn, currency_btn, consultant_btn)
    return admin_btn

currency_btn = InlineKeyboardMarkup(row_width=1)
yes_currency_btn = InlineKeyboardButton('Да', callback_data='currency_yes')
menu_btn = InlineKeyboardButton('Нет, вернуться в меню', callback_data='main_menu')
currency_btn.add(yes_currency_btn).add(menu_btn)

order_visa_btn = InlineKeyboardMarkup(row_width=1)
visa = InlineKeyboardButton('Посмотреть', callback_data='evisa_order')
order_visa_btn.add(visa)

order_charter_btn = InlineKeyboardMarkup(row_width=1)
charter = InlineKeyboardButton('Посмотреть', callback_data='charter_order')
order_charter_btn.add(charter)

order_hotel_btn = InlineKeyboardMarkup(row_width=1)
hotel = InlineKeyboardButton('Посмотреть', callback_data='hotel_order')
order_hotel_btn.add(hotel)

order_tour_btn = InlineKeyboardMarkup(row_width=1)
tour = InlineKeyboardButton('Посмотреть', callback_data='tour_order')
order_tour_btn.add(tour)

order_exchange_btn = InlineKeyboardMarkup(row_width=1)
exchange = InlineKeyboardButton('Посмотреть', callback_data='exchange_order')
order_exchange_btn.add(exchange)

order_consultant_btn = InlineKeyboardMarkup(row_width=1)
consultant = InlineKeyboardButton('Посмотреть', callback_data='consultant_order')
order_consultant_btn.add(consultant)

def gen_inline_visa_orders(data):
    urlkb_visa_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_visa_orders.add(InlineKeyboardButton(f'Заявка на оформление  E-Visa на {i[1]}',
                                                 callback_data=f'visa|{i[0]}|{i[1]}'))
    return urlkb_visa_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))


def gen_inline_charter_orders(data):
    urlkb_charter_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_charter_orders.add(InlineKeyboardButton(f'Чартер из {i[1]} в {i[2]} {i[3]}',
                                                 callback_data=f'one_charter|{i[0]}|{i[3]}'))
    return urlkb_charter_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))


def gen_inline_hotel_orders(data):
    urlkb_hotel_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_hotel_orders.add(InlineKeyboardButton(f'Отель в {i[1]} {i[5]} на {i[6]} ночей',
                                                 callback_data=f'one_hotel|{i[0]}|{i[5]}'))
    return urlkb_hotel_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))


def gen_inline_tour_orders(data):
    urlkb_tour_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_tour_orders.add(InlineKeyboardButton(f'Тур {i[1]} - {i[2]} {i[3]}',
                                                 callback_data=f'one_tour|{i[0]}|{i[3]}'))
    return urlkb_tour_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))


def gen_inline_exchange_orders(data):
    urlkb_exchange_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_exchange_orders.add(InlineKeyboardButton(f'Обмен {i[3]} {i[1]} на {i[4]} VND',
                                                 callback_data=f'one_exchange|{i[0]}|{i[3]}'))
    return urlkb_exchange_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))


def gen_inline_consultant_orders(data):
    urlkb_exchange_orders = InlineKeyboardMarkup(row_width=1)
    for i in data:
        urlkb_exchange_orders.add(InlineKeyboardButton(f'Консультация {i[0]}', callback_data=f'one_consultant|{i[0]}'))
    return urlkb_exchange_orders.add(InlineKeyboardButton('Назад', callback_data='admin_menu'))