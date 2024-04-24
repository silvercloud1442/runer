import sqlite3 as sql
from flask import Flask, request, g, jsonify
from datetime import datetime, timedelta
from telebot import types
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


def get_by_date():
    con = sql.connect('instance/base.db')
    cur = con.cursor()
    date = (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    cur.execute("select * from orders where end_date = '{}'".format(date))
    data = cur.fetchall()


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_by_date, trigger="interval", seconds=5)
atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app = Flask(__name__)


@app.route('/get_orders', methods=['POST', "GET"])
def hello_world():
    user_id = request.args.get('user_id')
    con = sql.connect('instance/base.db')
    cur = con.cursor()
    cur.execute(f'select * from orders where user_id = {user_id}')
    data = cur.fetchall()
    return data

@app.route("/request_to_report", methods=["POST", "GET"])
def request_to_report():
    user_id = request.args.get('user_id')
    worker_id = request.args.get('worker_id')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('1', callback_data=f'report_{worker_id}_{user_id}_1'))
    markup.add(types.InlineKeyboardButton('2', callback_data=f'report_{worker_id}_{user_id}_2'))
    markup.add(types.InlineKeyboardButton('3', callback_data=f'report_{worker_id}_{user_id}_3'))
    markup.add(types.InlineKeyboardButton('4', callback_data=f'report_{worker_id}_{user_id}_4'))
    markup.add(types.InlineKeyboardButton('5', callback_data=f'report_{worker_id}_{user_id}_5'))

    bot.send_message(user_id, 'Grade work', reply_markup=markup)
    return 'true'

# @app.route('/get', methods=["GET"])
# def get():
#     out = [
#     {
#         'id': user[0],
#         'phone': user[1],
#         'tg_id': user[2]
#     }
#     for user in query_db('select * from user')
#     ]
#     return jsonify(out)
#
# @app.route("/get_orders", methods=["POST", "GET"])
# def get_orders():
#     out = [{
#         'order number': order[1],
#         'recepient phone': order[4],
#         'end date': order[6]
#     }
#     for order in query_db(f'select * from orders where user_id = {request.args.get("user_id")}')
#     ]
#     return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True)
