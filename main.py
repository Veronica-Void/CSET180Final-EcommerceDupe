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

@app.route('/add_products', methods=['GET'])
def add_products():
    return render_template('add_products.html')


# @app.route('/add_products', methods=['POST'])
# def add_products_post():
#     session['username'] = 'test_user'
#     created_by = session['username']
#     conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, ADDED_BY_USERNAME) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': created_by})
#     conn.execute(text('INSERT INTO ProductImages (PID, imagesURL) VALUES (LAST_INSERT_ID(), :imagesURL)'), {'imagesURL': request.form['imagesURL']})
#     conn.execute(text('INSERT INTO ProductColor (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
#     conn.execute(text('INSERT INTO ProductSize (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
#     conn.commit()
#     return redirect('/add_products')

@app.route('/add_products', methods=['POST'])
def add_products_post():
    session['username'] = 'test_user'
    created_by = session['username']

    # Ensure the user exists in the USERS table
    user_exists = conn.execute(text('SELECT 1 FROM USERS WHERE USER_NAME = :username'), {'username': created_by}).fetchone() is not None
    if not user_exists:
        conn.execute(text('INSERT INTO USERS (USER_NAME, NAME) VALUES (:username, :name)'), {'username': created_by, 'name': 'Test User'})

    conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, ADDED_BY_USERNAME) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': created_by})
    conn.execute(text('INSERT INTO ProductImages (PID, imagesURL) VALUES (LAST_INSERT_ID(), :imagesURL)'), {'imagesURL': request.form['imagesURL']})
    conn.execute(text('INSERT INTO ProductColor (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
    conn.execute(text('INSERT INTO ProductSize (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
    conn.commit()
    return redirect('/add_products')

@app.route('/update', methods=['POST'])
def update_product():
    PID = request.form['PID']
    conn.execute(text('UPDATE PRODUCT SET TITLE = :title, DESCRIPTION = :description, WARRANTY_PERIOD = :warranty_period, NUMBER_OF_ITEMS = :number_of_items, PRICE = :price WHERE PID = :PID'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'PID': PID})
    conn.execute(text('UPDATE ProductImages SET imagesURL = :imagesURL WHERE PID = :PID'), {'imagesURL': request.form['imagesURL'], 'PID': PID})
    conn.execute(text('UPDATE ProductColor SET color = :color WHERE PID = :PID'), {'color': request.form['color'], 'PID': PID})
    conn.execute(text('UPDATE ProductSize SET size = :size WHERE PID = :PID'), {'size': request.form['size'], 'PID': PID})
    conn.commit()
    return redirect('/add_products')

@app.route('/delete', methods=['POST'])
def delete_product():
    PID = request.form['PID']
    # Delete related records first
    conn.execute(text('DELETE FROM ProductImages WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductColor WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductSize WHERE PID = :PID'), {'PID': PID})
    # Now delete the product
    conn.execute(text('DELETE FROM PRODUCT WHERE PID = :PID'), {'PID': PID})
    conn.commit()
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


# @app.route('/create_test', methods=['POST'])
# def create_test():
#     action = request.form.get('action')
#     if action == 'delete':
#         test_id = request.form.get('test_id')
#         # Delete associated rows from 'options' table
#         conn.execute(text(
#             'DELETE o FROM Options o JOIN Questions q ON o.question_id = q.question_id WHERE q.test_id = :test_id'),
#                      {'test_id': test_id})
#         # Delete associated rows from 'questions' table
#         conn.execute(text('DELETE FROM Questions WHERE test_id = :test_id'), {'test_id': test_id})
#         # Delete the test itself
#         conn.execute(text('DELETE FROM Test WHERE test_id = :test_id'), {'test_id': test_id})
#         conn.commit()
#         return render_template('create_test.html')
#     else:
#         # existing code for creating a test
#         teacher_id = int(flask_session.get('user_id'))
#         title = request.form.get('title')
#         duration = request.form.get('duration')
#         num_questions = int(request.form.get('num_questions'))
#         conn.execute(text('INSERT INTO Test (title, duration, teach_id) VALUES (:title, :duration, :teach_id)'),
#                      {'title': title, 'duration': duration, 'teach_id': teacher_id})
#         conn.commit()
#         test_id = conn.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]
#         for _ in range(num_questions):
#             num1 = random.randint(1, 10)
#             num2 = random.randint(1, 10)
#             question = f"What is {num1} + {num2}?"
#             correct_answer = num1 + num2
#             conn.execute(text(
#                 'INSERT INTO Questions (test_id, question, correct_option) VALUES (:test_id, :question, :correct_option)'),
#                          {'test_id': test_id, 'question': question, 'correct_option': correct_answer})
#             conn.commit()
#             question_id = conn.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]
#             incorrect_answers = [correct_answer + i for i in range(1, 4)]
#             random.shuffle(incorrect_answers)
#             for option in [correct_answer] + incorrect_answers:
#                 conn.execute(
#                     text('INSERT INTO Options (question_id, option_value) VALUES (:question_id, :option_value)'),
#                     {'question_id': question_id, 'option_value': option})
#                 conn.commit()
#         return render_template('create_test.html')
