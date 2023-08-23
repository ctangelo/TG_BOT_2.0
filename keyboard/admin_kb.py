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

order_exchange_btn = InlineKeyboardMarkup(row_width=1)
exchange = InlineKeyboardButton('Посмотреть', callback_data='exchange_order')
order_exchange_btn.add(exchange)

order_consultant_btn = InlineKeyboardMarkup(row_width=1)
consultant = InlineKeyboardButton('Посмотреть', callback_data='consultant_order')
order_consultant_btn.add(consultant)


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