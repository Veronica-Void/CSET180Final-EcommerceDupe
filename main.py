from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.
import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.
from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
from sqlalchemy import create_engine, text
import hashlib

c_str = "mysql://root:cyber241@localhost/ecomm"
engine = create_engine(c_str, echo=True)
conn = engine.connect()

app = Flask(__name__)
app.secret_key = 'hola'

@app.route('/')
def home():
    return render_template('index.html')


def product():
    products = product.query.all()
    return render_template('product.html', products=products)


@app.route('/product/<pid>')
def product_detail(pid):
    product = product.query.filter_by(PID=pid).first()
    return render_template('product_detail.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)

