from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from telebot import types
import telebot

token = '7076655539:AAEyzHEHJLyjOOESREFPprLGbPIMDls6oxA'
bot = telebot.TeleBot(token)

app = Flask(__name__)
app.config["SECRET_KEY"] = "bimbimbambam"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    phone = db.Column(db.String(15), nullable=False)
    telegram_id = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return "<{0} : {1}>".format(self.phone, self.telegram_id)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<{0} : {1}>".format(self.description, self.date)

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

# @app.route("/get_user", methods=["GET"])
# def get_user():
#     users = User.query.all()
#     out = [
#         {
#             "id" : user.id,
#             "phone" : user.phone,
#             "telegram_id" : user.telegram_id
#         }
#         for user in users
#     ]
#     return jsonify(out)

@app.route("/get_orders", methods=["POST", "GET"])
def get_orders():
    user = User.query.filter(User.telegram_id == request.args.get('telegram_id')).first()
    orders = Order.query.filter(Order.user_id == user.id)
    out = [
        {
            'order description': order.description,
        }
        for order in orders
    ]
    return jsonify(out)

@app.route("/")
def home():
    return 'bimbimbambam'

if __name__ == '__main__':
    app.run(debug=True, host="192.168.77.86")
