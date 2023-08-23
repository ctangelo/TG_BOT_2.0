import sqlite3 as sq
from dispatcher import bot
from handlers.admin import ID
from keyboard.admin_kb import order_exchange_btn, order_consultant_btn

def sql_start():
    global base, cur
    base = sq.connect('clients.db')
    cur = base.cursor()
    if base:
        print("Database connected successfully")
    # base.execute('DROP TABLE exchange')
    base.execute('CREATE TABLE IF NOT EXISTS exchange(user_id INTEGER, currency TEXT, bank TEXT, amount INTEGER, vnd_amount INTEGER, aprove TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS currency(rub INTEGER, kzt INTEGER, kgs INTEGER, uzs INTEGER, usdt INTEGER)')
    base.execute('CREATE TABLE IF NOT EXISTS consultant(user_id INTEGER)')
    base.commit()

# ____________CONSULTANT_____________________________


async def add_consultant(user_id):
    with base:
        cur.execute('INSERT INTO consultant VALUES (?)', (user_id, ))
    await bot.send_message(ID, 'У вас новая заявка консультацию', reply_markup=order_consultant_btn)


async def one_consultant(user_id):
    with base:
        cur.execute('SELECT * FROM consultant WHERE user_id=?', (user_id, ))
        return cur.fetchone()


async def all_consultant():
    with base:
        cur.execute('SELECT * FROM consultant')
        return cur.fetchall()
    
async def delete_consultant(user_id):
    with base:
        cur.execute('DELETE FROM consultant WHERE user_id=?', (user_id, ))
    
    
def count_consultant():
    with base:
        cur.execute('SELECT COUNT(user_id) FROM consultant')
        return cur.fetchone()

    
# ____________exchange_____________________________

def count_exchange():
    with base:
        cur.execute('SELECT COUNT(user_id) from exchange')
        return cur.fetchone()[0]


async def add_exchange(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO exchange VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()
    await bot.send_message(ID, 'У вас новая заявка на обмен валюты', reply_markup=order_exchange_btn)


async def see_exchange():
    with base:
        cur.execute('SELECT * FROM exchange')
        return cur.fetchall()
    

async def one_exchange(user_id, amount):
    with base:
        cur.execute(f'SELECT * FROM exchange WHERE (user_id = ?) AND (amount = ?)', (user_id, amount))
        return cur.fetchone()


async def delete_exchange(user_id, amount):
    with base:
        cur.execute('DELETE FROM exchange WHERE (user_id = ?) AND (amount = ?)', (user_id, amount))

# ____________currency_____________________________


async def add_currency(state):
    async with state.proxy() as data:
        cur.execute('DELETE FROM currency')
        cur.execute('INSERT INTO currency VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

def check_currency(currency):
    with base:
        cur.execute(f'SELECT {currency} FROM currency')
        return cur.fetchone()[0]
    