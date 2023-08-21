from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from dispatcher import bot


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(main_kb)

back_btn = InlineKeyboardMarkup(row_width=1)
back = InlineKeyboardButton('Назад', callback_data='main_menu')
back_btn.add(back)

inline_menu = InlineKeyboardMarkup(row_width=1)
inline_advantages_btn = InlineKeyboardButton('Наши преимущества', callback_data='advantages')
inline_how_it_works_btn = InlineKeyboardButton('Как это работает?', callback_data='how_it_works')
inline_exchange_btn = InlineKeyboardButton('💰 Обмен валюты', callback_data='exchange')
inline_calculator_btn = InlineKeyboardButton('🧮 Калькулятор Обмена', callback_data='calculator')
inline_reviews_btn = InlineKeyboardButton('Отзывы', callback_data='reviews')
inline_consultant_btn = InlineKeyboardButton('👨‍💻 Консультация менеджера', callback_data='consultant')
inline_menu.add(inline_advantages_btn).add(inline_how_it_works_btn).add(inline_exchange_btn).add(inline_calculator_btn).add(inline_reviews_btn).add(inline_consultant_btn)

# __________________Обмен валюты_________________________

exchange_btn = InlineKeyboardMarkup(row_width=1)
yes_exchange_btn = InlineKeyboardButton('Да', callback_data='exchange_yes')
no_exchange_btn = InlineKeyboardButton('Нет, вернуться в меню', callback_data='main_menu')
exchange_btn.add(yes_exchange_btn).add(no_exchange_btn)

currency_btn = InlineKeyboardMarkup(row_width=1)
rub_btn = InlineKeyboardButton('RUB', callback_data='rub')
kzt_btn = InlineKeyboardButton('KZT', callback_data='kzt')
kgs_btn = InlineKeyboardButton('KGS', callback_data='kgs')
uzs_btn = InlineKeyboardButton('UZS', callback_data='uzs')
usdt_btn = InlineKeyboardButton('USDT', callback_data='usdt')
currency_btn.row(rub_btn, kzt_btn, kgs_btn, uzs_btn, usdt_btn)

def choose_bank_btn(currency):
    if currency == 'rub':
        bank_btn = InlineKeyboardMarkup(row_width=1)
        sber = InlineKeyboardButton('Сбербанк', callback_data='сбербанк')
        tinkof = InlineKeyboardButton('Тинькофф', callback_data='Тинькофф')
        alfa = InlineKeyboardButton('Альфа-банк', callback_data='Альфа-банк')
        raif = InlineKeyboardButton('Райффайзенбанк', callback_data='Райффайзенбанк')
        bank_btn.add(sber, tinkof, alfa, raif)

    elif currency == 'kzt':
        bank_btn = InlineKeyboardMarkup(row_width=1)
        kaspi = InlineKeyboardButton('Kaspi Bank', callback_data='Kaspi Bank')
        jusan = InlineKeyboardButton('Jusan Bank', callback_data='Jusan Bank')
        freedom = InlineKeyboardButton('Freedom Bank', callback_data='Freedom Bank')
        bank_btn.add(kaspi, jusan, freedom)

    elif currency == 'kgs':
        bank_btn = InlineKeyboardMarkup(row_width=1)
        mbank = InlineKeyboardButton('MBank', callback_data='MBank')
        demir = InlineKeyboardButton('Demir', callback_data='Demir')
        bank_btn.add(mbank, demir)

    if currency == 'uzs':
        bank_btn = InlineKeyboardMarkup(row_width=1)
        kapital = InlineKeyboardButton('KapitalBank', callback_data='KapitalBank')
        uzum = InlineKeyboardButton('Uzum Bank', callback_data='Uzum Bank')
        humo = InlineKeyboardButton('Humo', callback_data='Humo')
        uzcard = InlineKeyboardButton('UzCard', callback_data='UzCard')
        bank_btn.add(kapital, uzum, humo, uzcard)

    return bank_btn




# exchange_cities = InlineKeyboardMarkup(row_width=1)
# nha_trang = InlineKeyboardButton('Нячанг', callback_data='нячанг')
# muyne = InlineKeyboardButton('Муйне', callback_data='муйне')
# phukok = InlineKeyboardButton('о.Фукуок', callback_data='о.фукуок')
# danang = InlineKeyboardButton('Дананг', callback_data='дананг')
# hochimin = InlineKeyboardButton('Хошимин', callback_data='хошимин')
# hanoi = InlineKeyboardButton('Ханой', callback_data='ханой')
# exchange_cities.row(nha_trang, phukok, muyne) 
# exchange_cities.row(danang, hochimin, hanoi)

# exchange_delivery = InlineKeyboardMarkup(row_width=1)
# delivery_cash = InlineKeyboardButton('Доставка наличные', callback_data='доставка наличные')
# pickup = InlineKeyboardButton('Самовывоз', callback_data='самовывоз')
# atm = InlineKeyboardButton('Получить через банкомат', callback_data='банкомат')
# exchange_delivery.add(delivery_cash, pickup, atm)

approve_btn = InlineKeyboardMarkup(row_width=1)
approve = InlineKeyboardButton('Подтвердить', callback_data='aprove')
decline = InlineKeyboardButton('Отменить', callback_data='decline')
approve_btn.add(approve, decline)