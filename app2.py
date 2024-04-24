import sqlite3
from flask import Flask, request, g, jsonify
import psycopg2

# Create a Flask app
app = Flask(__name__)

# Connect to the database using psycopg2 library and the database credentials
base = 'instance/base.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(base)
    return db


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


# @app.route('/create', methods=['POST'])
# def create():
#     # Get the username and email from the request body
#     username = request.form.get('username')
#     email = request.form.get('email')
#
#     # Insert the data into the database
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
#     conn.commit()
#
#     return 'User created successfully!'

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/get', methods=["GET"])
def get():
    out = [
    {
        'id': user[0],
        'phone': user[1],
        'tg_id': user[2]
    }
    for user in query_db('select * from user')
    ]
    return jsonify(out)

@app.route("/get_orders", methods=["POST", "GET"])
def get_orders():
    out = [{
        'order number': order[1],
        'recepient phone': order[4],
        'end date': order[6]
    }
    for order in query_db(f'select * from orders where user_id = {request.args.get("user_id")}')
    ]
    return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True)
