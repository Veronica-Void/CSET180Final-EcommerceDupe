

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text
# from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker
from flask import session as flask_session

app = Flask(__name__)
app.secret_key = 'password123'
connect = "mysql://root:Applepine13.!@localhost/ECOM"
engine = create_engine(connect, echo=True)







# i keep getting a yellow error whenever I uncomment this import - Vee
# from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.

import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.

from flask import Flask, render_template, request, redirect, session, url_for, flash #imported flask and other things here
# from flask import session as session

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import hashlib

c_str = "mysql://root:cyber241@localhost/ecomm"
engine = create_engine(c_str, echo=True)

conn = engine.connect()




# displays the home page
@app.route('/')
def home():
    return render_template('/index.html')

# ------------------------------------------------ Start of Register ------------------------------------------------------------

# this function is used in registerUser to hash the password when it is entered by the user and add it to the db
def hash_password(inputpw):
    return hashlib.sha3_256(inputpw.encode())

def Checkexist(user_name):
     user_name = str(user_name)
     account = conn.execute(text("SELECT USER_NAME FROM USER WHERE USER_NAME = :USER_NAME"), {'USER_NAME': user_name})
     result = account.fetchone()
     if result:
         return True
     else:
        return False

# displays the sign up page
@app.route('/register', methods=['GET'])
def showRegister():
    return render_template('/register.html')

# actual sign up function
@app.route('/register', methods=['POST', 'GET'])
def registerUser():
    msg = ''
    if request.method == 'POST':
        user_name = request.form.get('USER_NAME')
        name = request.form.get('NAME')
        email = request.form.get('EMAIL')
        password = request.form.get('PASSWORD')
        acc_type = request.form.get('ACCOUNT_TYPE')
        # hashing the password value
        hashed_password = hash_password(password).hexdigest()

        if Checkexist(user_name):
            flash('This Account Already Exists!', 'error')
            return redirect(url_for('showRegister'))
        else:
            conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', \'{acc_type}\')'))
            conn.commit() #extra layer of protection
            session['loggedin'] = True
            session['USER_NAME'] = user_name
            session["NAME"] = f"{name}"  
            return redirect(url_for('showLogin'))   

# ------------------------------------------------ End of Register ------------------------------------------------------------


# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
# function uses session to display errors when there is a bad login attempt
def showLogin():
  return render_template('/login.html')


@app.route('/login', methods=['POST', 'GET'])
# actual login function 

def loginUser():
    msg = ''
    if request.method == 'POST' and 'USER_NAME' in request.form and 'PASSWORD' in request.form:
        username = request.form.get('USER_NAME')
        password = request.form.get('PASSWORD')

        hashed_password = hash_password(password).hexdigest()

        account = conn.execute(text("SELECT * FROM User WHERE USER_NAME = :user_name AND PASSWORD = :hashed_password"), {'user_name': username, 'hashed_password': hashed_password})
        user_data = account.fetchone()
         
        if user_data:
            session['loggedin'] = True
            session['USER_NAME'] = user_data[0]
            session['NAME'] = f"{user_data[1]}"
            if user_data[4] == 'Admininstrator':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            msg = 'Wrong username or password'

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('USER_NAME', None)
    session.pop('NAME', None)
    return redirect(url_for('loginUser'))

# ------------------------------------------------ End of Login ----------------------------------------------------------------



# -- Start of Log out --








# -- End of log out --




# ------------------------------------------------ Start of User Accounts ------------------------------------------------------------

@app.route('/my_account', methods=['GET'])
def account_info():
    username = str(session.get('USER_NAME'))
    if username:
        account = conn.execute(text("SELECT * FROM user WHERE USER_NAME = :USER_NAME"), {'USER_NAME': username})
        user_data = account.fetchone()
        if user_data:
            return render_template("my_account.html", user_data=user_data)
    return redirect(url_for('login'))

# ------------------------------------------------ End of User Accounts --------------------------------------------------------------





# ------------------------------------------------ Start of Admin ------------------------------------------------------------

# temporary view of admin
@app.route('/admin')
def showAdmin():
    return render_template('/admin.html')

# ------------------------------------------------ End of Admin --------------------------------------------------------------




# ------------------------------------------------ Start of Product ------------------------------------------------------------













# ------------------------------------------------ End of Product ------------------------------------------------------------


























































































## Start of Vendor functions
@app.route('/add_products', methods=['GET'])
def add_products():
    return render_template('add_products.html')




@app.route('/add_products', methods=['POST'])
def add_products_post():
    # session['user_id'] = 'test_user'
    created_by = flask_session['user_id']

    # Ensure the user exists in the USERS table
    user_exists = conn.execute(text('SELECT 1 FROM USERS WHERE USER_NAME = :username'), {'username': created_by}).fetchone() is not None
    if not user_exists:
        conn.execute(text('INSERT INTO USERS (USER_NAME, NAME) VALUES (:username, :name)'), {'username': created_by, 'name': 'Test User'})

    conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, ADDED_BY_USERNAME, Category) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by, :category)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': created_by, 'category': request.form['category']})
    conn.execute(text('INSERT INTO ProductImages (PID, imagesURL) VALUES (LAST_INSERT_ID(), :imagesURL)'), {'imagesURL': request.form['imagesURL']})
    conn.execute(text('INSERT INTO ProductColor (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
    conn.execute(text('INSERT INTO ProductSize (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
    conn.commit()
    return redirect('/add_products')




@app.route('/update', methods=['POST'])
def update_product():
    PID = request.form['PID']
    # category = request.form['category']
    conn.execute(text('UPDATE PRODUCT SET TITLE = :title, DESCRIPTION = :description, WARRANTY_PERIOD = :warranty_period, NUMBER_OF_ITEMS = :number_of_items, PRICE = :price, Category = :category WHERE PID = :PID'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'],'category': request.form['category'], 'PID': PID,})
    conn.execute(text('UPDATE ProductImages SET imagesURL = :imagesURL WHERE PID = :PID'), {'imagesURL': request.form['imagesURL'], 'PID': PID})
    conn.execute(text('UPDATE ProductColor SET color = :color WHERE PID = :PID'), {'color': request.form['color'], 'PID': PID})
    conn.execute(text('UPDATE ProductSize SET size = :size WHERE PID = :PID'), {'size': request.form['size'], 'PID': PID})
    conn.commit()
    return redirect('/add_products')


@app.route('/delete', methods=['POST'])
def delete_product():
    created_by = flask_session['user_id']
    PID = request.form['PID']
    conn.execute(text('DELETE FROM Review WHERE Product = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductImages WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductColor WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductSize WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT WHERE PID = :PID and ADDED_BY_USERNAME = :created_by'), {'PID': PID, 'created_by': created_by})
    conn.commit()
    return redirect('/add_products')

## End of Vendor functions

@app.route('/product_page', methods=['GET'])
def view_products():
    pass

@app.route('/product_page', methods=['POST'])
def view_products_post():   
    pass


## Start of admin functions
@app.route('/admin_add_products', methods=['GET'])
def admin_add_products():
    return render_template('admin_add_products.html')


@app.route('/admin_add_products', methods=['POST'])
def admin_add_products_post():
    created_by = request.form['vendor_username']

    # Ensure the user exists in the USERS table
    user_exists = conn.execute(text('SELECT 1 FROM USERS WHERE USER_NAME = :username'), {'username': created_by}).fetchone() is not None
    if not user_exists:
        conn.execute(text('INSERT INTO USERS (USER_NAME, NAME) VALUES (:username, :name)'), {'username': created_by, 'name': 'Vendor'})
    conn.execute(text('INSERT INTO PRODUCT (TITLE, DESCRIPTION, WARRANTY_PERIOD, NUMBER_OF_ITEMS, PRICE, ADDED_BY_USERNAME, Category) VALUES (:title, :description, :warranty_period, :number_of_items, :price, :created_by, :category)'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'], 'created_by': created_by, 'category': request.form['category']})
    conn.execute(text('INSERT INTO ProductImages (PID, imagesURL) VALUES (LAST_INSERT_ID(), :imagesURL)'), {'imagesURL': request.form['imagesURL']})
    conn.execute(text('INSERT INTO ProductColor (PID, color) VALUES (LAST_INSERT_ID(), :color)'), {'color': request.form['color']})
    conn.execute(text('INSERT INTO ProductSize (PID, size) VALUES (LAST_INSERT_ID(), :size)'), {'size': request.form['size']})
    conn.commit()
    return redirect('/admin_add_products')


@app.route('/all_accounts', methods=['GET'])
def all_accounts():
    return render_template('all_accounts.html')


@app.route('/all_accounts', methods=['POST'])
def search_account():
    acc_type = request.form.get('acc_type')
    if acc_type == 'all':
        users = conn.execute(text('SELECT * FROM USER')).fetchall()
    else:
        users = conn.execute(text('SELECT * FROM USER WHERE ACCOUNT_TYPE = :acc_type'), {'acc_type': acc_type}).fetchall()
    conn.commit()
    print(users)
    return render_template('all_accounts.html', users=users)



@app.route('/admin_update', methods=['POST'])
def admin_update_product():
    created_by = request.form['vendor_username']
    PID = request.form['PID']
    # category = request.form['category']
    conn.execute(text('UPDATE PRODUCT SET TITLE = :title, DESCRIPTION = :description, WARRANTY_PERIOD = :warranty_period, NUMBER_OF_ITEMS = :number_of_items, PRICE = :price, Category = :category WHERE PID = :PID'), {'title': request.form['title'], 'description': request.form['description'], 'warranty_period': request.form['warranty_period'], 'number_of_items': request.form['number_of_items'], 'price': request.form['price'],'category': request.form['category'], 'PID': PID,})
    conn.execute(text('UPDATE ProductImages SET imagesURL = :imagesURL WHERE PID = :PID'), {'imagesURL': request.form['imagesURL'], 'PID': PID})
    conn.execute(text('UPDATE ProductColor SET color = :color WHERE PID = :PID'), {'color': request.form['color'], 'PID': PID})
    conn.execute(text('UPDATE ProductSize SET size = :size WHERE PID = :PID'), {'size': request.form['size'], 'PID': PID})
    conn.commit()
    return redirect('/admin_add_products')


@app.route('/admin_delete', methods=['POST'])
def admin_delete_product():
    PID = request.form['PID']
    created_by = request.form['vendor_username']
    conn.execute(text('DELETE FROM ProductImages WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductColor WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM ProductSize WHERE PID = :PID'), {'PID': PID})
    conn.execute(text('DELETE FROM PRODUCT WHERE PID = :PID AND ADDED_BY_USERNAME = :username'), {'PID': PID, 'username': created_by})
    conn.commit()
    return redirect('/admin_add_products')
## End of admin functions






## Start of review section
@app.route('/review',methods=['GET'])
def review_get():
    return render_template('review.html')


@app.route('/review',methods=['POST'])
def review_post():
    username = flask_session['user_id']
    rating = request.form['rating']
    desc = request.form['desc']
    img = request.form['img']
    Product = request.form['Product']
    conn.execute(text('INSERT INTO REVIEW (RATING, `DESC`, IMG, REVIEW_USER_NAME,Product) VALUES (:rating, :desc, :img, :username, :Product)'), {'rating': rating, 'desc': desc, 'img': img, 'username': username, 'Product': Product})
    conn.commit()
    return redirect('/review')


@app.route('/view_reviews', methods=['GET'])
def view_reviews():
    return render_template('view_reviews.html')


@app.route('/view_reviews', methods=['POST'])
def view_reviews_post():
    Product = request.form.get('Product')
    Rating = request.form.get('Rating')
    if Product and Rating:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE Product = :Product AND RATING = :Rating'), {'Product': Product, 'Rating': Rating}).fetchall()
    elif Product:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE Product = :Product'), {'Product': Product}).fetchall()
    elif Rating:
        reviews = conn.execute(text('SELECT * FROM REVIEW WHERE RATING = :Rating'), {'Rating': Rating}).fetchall()
    else:
        reviews = conn.execute(text('SELECT * FROM REVIEW')).fetchall()
    conn.commit()
    return render_template('view_reviews.html', reviews=reviews)
## End of review section


@app.route('/product_page', methods=['GET'])
def product_page_get():
    return render_template('product_page.html')


@app.route('/product_page', methods=['POST'])
def product_page_post():
    pass

##

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')




@app.route('/register', methods=['POST'])
def create_user():
    conn.execute(text('INSERT INTO USER VALUES (:username, :Name, :Email, :Password, :Account_Type)'), request.form)
    conn.commit()
    return render_template('login.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    with app.app_context():
        engine = create_engine(connect)
        Session = sessionmaker(bind=engine)
        session = Session()
        conn = engine.connect()

        user = session.execute(text('SELECT USER_NAME, ACCOUNT_TYPE FROM USER WHERE USER_NAME = :username AND PASSWORD = :password'),
                               request.form).fetchone()
        session.commit()
        conn.commit()

        if user:
            if user.ACCOUNT_TYPE == 'Administrator':
                admin = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and ACCOUNT_TYPE = "Administrator"'),
                        {'username': user.USER_NAME}).fetchone()
                flask_session['user_id'] = admin.USER_NAME  # Store the admins id in the session
                return render_template('admin_add_products.html')
            elif user.ACCOUNT_TYPE == 'Customer':
                customer = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and ACCOUNT_TYPE = "Customer" '),
                                           {'username': user.USER_NAME}).fetchone()
                flask_session['user_id'] = customer.USER_NAME  # Store the student's ID in the session
                # flask_session['customer_id'] = customer.CustomerID  # Store the student's ID in the session

                return render_template('customer.html')
            elif user.ACCOUNT_TYPE == 'Vendor':
                vendor = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and ACCOUNT_TYPE = "Vendor"'),
                                         {'username': user.USER_NAME}).fetchone()
                flask_session['user_id'] = vendor.USER_NAME
                return render_template('add_products.html')
        
        else:
            invalid = "Invalid email or password"
            return render_template('login.html', invalid=invalid)
        




    


   











    

    

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




# @app.route('/login', methods=['GET'])
# def login():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login_post():
#     with app.app_context():
#         engine = create_engine(connect)
#         Session = sessionmaker(bind=engine)
#         session = Session()
#         conn = engine.connect()

#         user = session.execute(text('SELECT USER_NAME, ACCOUNT_TYPE FROM USER WHERE USER_NAME = :username AND PASSWORD = :password'),
#                                request.form).fetchone()
#         session.commit()
#         conn.commit()

#         if user:
#             if user.ACCOUNT_TYPE == 'Administrator':
#                 admin = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and and ACCOUNT_TYPE = Administrator'),
#                                         {'username': user.USER_NAME}).fetchone()
#                 flask_session['user_id'] = admin.USER_NAME  # Store the admins id in the session
#                 return render_template('admin.html')
#             elif user.ACCOUNT_TYPE == 'Customer':
#                 customer = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and ACCOUNT_TYPE = Customer '),
#                                            {'username': user.USER_NAME}).fetchone()
#                 flask_session['user_id'] = customer.USER_NAME  # Store the student's ID in the session
#                 # flask_session['customer_id'] = customer.CustomerID  # Store the student's ID in the session

#                 return render_template('customer.html')
#             elif user.ACCOUNT_TYPE == 'Vendor':
#                 vendor = session.execute(text('SELECT * FROM USER WHERE USER_NAME = :username and ACCOUNT_TYPE = Vendor'),
#                                          {'username': user.USER_NAME}).fetchone()
#                 flask_session['user_id'] = vendor.USER_NAME
#                 return render_template('vendor.html')
        
#         else:
#             invalid = "Invalid email or password"
#             return render_template('login.html', invalid=invalid)
        

# @app.route('/login', methods=['POST'])
# # taking values from Session and using them as a comparison to allow access
# def loginUser():
#     # starts the session (?)
#     with app.app_context():
#         session = sessionmaker(bind=engine) 

#         # changed the name of the variable from the example in discord
#         login_session = session()

#         # grabbing the password from the login form
#         Input_password = request.form.get('PASSWORD')

#         # hashing the password from the login form
#         hashInput_password = hash_password(Input_password).hexdigest()

#         # using the username in the session to grab info from the database
#         matchInput_username = session.execute(text(f'SELECT USER_NAME, ACCOUNT_TYPE FROM USER WHERE USER_NAME = :USER_NAME AND PASSWORD = \'{hashInput_password}\''), request.form).fetchone()
#         login_session.commit()
#         conn.commit()

#         # checks if user is admin, then brings admin to their pages
#         if matchInput_username.ACCOUNT_TYPE == 'administrator' or matchInput_username.ACCOUNT_TYPE == 'Administrator':
#             admin = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

#             # check to see if the user exists, if not display error message
#             if len(matchInput_username) < 1:
#                 flask_session['attemptError'] = 'This user does not exist, Please register the account and try again.'
#                 return redirect(url_for('showLogin'))

#             # displays message upon successful login 
#             elif len(matchInput_username) == 1:
#                 flask_session['attemptSuccess'] = 'Login Success!'
#                 # storing the admin's user_name in the session
#                 flask_session['user_data'] = login_session.USER_NAME 
#                 return redirect(url_for('showAdmin'))
        

#         # checks if user is customer, then brings customer to their pages
#         elif matchInput_username.ACCOUNT_TYPE == 'customer' or matchInput_username.ACCOUNT_TYPE == 'Customer':
#             customer = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

#             # check to see if the user exists, if not display error message
#             if len(matchInput_username) < 1:
#                 flask_session['attemptError'] = 'This user does not exist, Please register the account and try again.'
#                 return redirect(url_for('showLogin'))
            
#             # displays message upon successful login 
#             elif len(matchInput_username) == 1:
#                 flask_session['attemptSuccess'] = 'Login Success!'
#                 # storing the customer's user_name in the session
#                 flask_session['user_data'] = login_session.USER_NAME
#                 return redirect(url_for('showUser'))
        
        
#         # checks if user is vendor and brings them to vendor pages
#         elif matchInput_username.ACCOUNT_TYPE == 'vendor' or matchInput_username.ACCOUNT_TYPE == 'Vendor':
#             vendor = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

#             # check to see if the user exists, if not display error message
#             if len(matchInput_username) < 1:
#                 flask_session['attemptError'] = 'This user does not exist, Please register the account and try again.'
#                 return redirect(url_for('showLogin'))
            
#             # displays message upon successful login 
#             elif len(matchInput_username) == 1:
#                 flask_session['attemptSuccess'] = 'Login Success!'
#                 # stores the vendor's user_name in the session
#                 flask_session['user_data'] = login_session.USER_NAME
#                 return redirect(url_for('showVendor'))

 
#         else:
#             invalid = "This username or password is invalid, please try again."
#             return render_template('/login.html', invalid





# @app.route('/register', methods=['GET'])
# def register():
#     return render_template('register.html')


# @app.route('/register', methods=['POST'])
# def create_user():
#     conn.execute(text('INSERT into user(user_name,`name`,email,`password`,Account_type)',request.form))
#     conn.commit()
#     return render_template('Customer_create.html')