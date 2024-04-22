from random import random, randint

from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker
from flask import session as flask_session

app = Flask(__name__)
app.secret_key = 'password123'
connect = "mysql://root:Applepine13.!@localhost/ECOM"
engine = create_engine(connect, echo=True)
conn = engine.connect()



@app.route('/base')
def add():
    return render_template('base.html')


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('add_products', methods=['GET'])
def add_products():
    return render_template('add_products.html')


@app.route('/add_products', methods=['POST'])
def add_products_post():
    conn.execute('INSERT INTO PRODUCT (PID, TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, ADDED_BY_USERNAME) VALUES (:PID, :TITLE, :DESCRIPTION, :WARRANTY_PERIOD, :NUMBER_OF_ITEMS, :PRICE, :ADDED_BY_USERNAME)', PID=request.form['PID'], TITLE=request.form['TITLE'], DESCRIPTION=request.form['DESCRIPTION'], WARRANTY_PERIOD=request.form['WARRANTY_PERIOD'], NUMBER_OF_ITEMS=request.form['NUMBER_OF_ITEMS'], PRICE=request.form['PRICE'], ADDED_BY_USERNAME=request.form['ADDED_BY_USERNAME'])
    conn.execute('INSERT INTO ProductImages (PID, imagesURL) VALUES (:PID, :imagesURL)', PID=request.form['PID'], imagesURL=request.form['imagesURL'])
    conn.execute('INSERT INTO ProductColor (PID, color) VALUES (:PID, :color)', PID=request.form['PID'], color=request.form['color'])
    conn.execute('INSERT INTO ProductSize (PID, size) VALUES (:PID, :size)', PID=request.form['PID'], size=request.form['size'])
    return redirect('/add_products')











if __name__ == '__main__':
    app.run(debug=True)


# CREATE TABLE PRODUCT(
# PID VARCHAR(50) PRIMARY KEY,
# TITLE VARCHAR(50) NOT NULL,
# DESCRIPTION VARCHAR (400),
# WARRANTY_PERIOD INT,
# NUMBER_OF_ITEMS INT,
# PRICE FLOAT,
# ADDED_BY_USERNAME VARCHAR (50),
# FOREIGN KEY (ADDED_BY_USERNAME) REFERENCES USERS(USER_NAME)
# );

# create table ProductImages(
# PID varchar(50),
# FOREIGN KEY (PID) REFERENCES Product(PID),
# imagesURL varchar(200) not null
# );


# create table ProductColor(
# PID varchar(50),
# FOREIGN KEY (PID) REFERENCES Product(PID),
# color varchar(20) not null
# );


# create table ProductSize(
# PID varchar(50),
# FOREIGN KEY (PID) REFERENCES Product(PID),
# size varchar(10)
# );