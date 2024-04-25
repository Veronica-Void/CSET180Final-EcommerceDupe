# i keep getting a yellow error whenever I uncomment this import - Vee
# from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.

import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.
from flask import Flask, render_template, request, redirect, session, url_for, flash, get_flashed_messages, flask_session #imported flask and other things here
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import hashlib

c_str = "mysql://root:MySQL8090@localhost/ecomm"
engine = create_engine(c_str, echo=True)

conn = engine.connect()

app = Flask(__name__)
app.secret_key = 'hola'




# displays the home page
@app.route('/')
def home():
    return render_template('/index.html')

# ------------------------------------------------ Start of Register ------------------------------------------------------------

# this function is used in registerUser to hash the password when it is entered by the user and add it to the db
def hash_password(inputpw):
    return hashlib.sha3_256(inputpw.encode())

# displays the sign up page
@app.route('/register', methods=['GET'])
def showRegister():
    return render_template('/register.html')

# actual sign up function
# add session here too? idk bruh
@app.route('/register', methods=['POST'])
def registerUser():
    # grabbing the values that the user puts into the sign up form
    user_name = request.form.get('USER_NAME')
    name = request.form.get('NAME')
    email = request.form.get('EMAIL')
    password = request.form.get('PASSWORD')

    # hashing the password value
    hashed_password = hash_password(password).hexdigest()

    # inserting values including hashed password into the database
    conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', null)'))
    conn.commit() #extra layer of protection

    # if account type != 'admin' or account type != 'vendor', alter table to change account type to 'customer'
    # if account type != 'customer' or account type != 'admin', alter table to change account type to 'vendor'

    # NEED TO MAKE A CHECK FOR IF THE USER ALREADY EXISTS AND DISPLAY ERROR MESSAGE 

    return redirect(url_for('showLogin'))
# ------------------------------------------------ End of Register ------------------------------------------------------------




# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
# function uses session to display errors when there is a bad login attempt
def showLogin():
    if 'attemptError' in session:
        errorMessage = session.pop('attemptError')

    if 'attemptSuccess' in session:
        successMessage = session.pop('attemptSuccess')

    else:
        # setting empty variables because a nulls value can't be passed here
        errorMessage = ""
        successMessage = ""
    return render_template('/login.html', attemptError=errorMessage, attemptSuccess=successMessage)



@app.route('/login', methods=['POST'])
# taking values from Session and using them as a comparison to allow access
def loginUser():
    # starts the session (?)
    with app.app_context():
        engine = create_engine(conn)
        session = sessionmaker(bind=engine) 

        # changed the name of the variable from the example in discord
        login_session = session()
        conn = engine.connect()

        # grabbing the password from the login form
        Input_password = request.form.get('PASSWORD')

        # hashing the password from the login form
        hashInput_password = hash_password(Input_password).hexdigest()

        # using the username in the session to grab info from the database
        matchInput_username = session.execute(text(f'SELECT USER_NAME, ACCOUNT_TYPE FROM USER WHERE USER_NAME = :USER_NAME AND PASSWORD = \'{hashInput_password}\''), request.form).fetchone()
        login_session.commit()
        conn.commit()

        # checks if user is admin, then brings admin to their pages
        if matchInput_username.ACCOUNT_TYPE == 'administrator' or matchInput_username.ACCOUNT_TYPE == 'Administrator':
            admin = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

            # check to see if the user exists, if not display error message
            if len(matchInput_username) < 1:
                session['attemptError'] = 'This user does not exist, Please register the account and try again.'
                return redirect(url_for('showLogin'))

            # displays message upon successful login 
            elif len(matchInput_username) == 1:
                session['attemptSuccess'] = 'Login Success!'
                # storing the admin's user_name in the session
                flask_session['user_data'] = login_session.USER_NAME 
                return redirect(url_for('showAdmin'))
        

        # checks if user is customer, then brings customer to their pages
        elif matchInput_username.ACCOUNT_TYPE == 'customer' or matchInput_username.ACCOUNT_TYPE == 'Customer':
            customer = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

            # check to see if the user exists, if not display error message
            if len(matchInput_username) < 1:
                session['attemptError'] = 'This user does not exist, Please register the account and try again.'
                return redirect(url_for('showLogin'))
            
            # displays message upon successful login 
            elif len(matchInput_username) == 1:
                session['attemptSuccess'] = 'Login Success!'
                # storing the customer's user_name in the session
                flask_session['user_data'] = login_session.USER_NAME
                return redirect(url_for('showUser'))
        
        
        # checks if user is vendor and brings them to vendor pages
        elif matchInput_username.ACCOUNT_TYPE == 'vendor' or matchInput_username.ACCOUNT_TYPE == 'Vendor':
            vendor = login_session.execute(text('SELECT * FROM USER WHERE USER_NAME = :USER_NAME'), {'USER_NAME': login_session.USER_NAME}).fetchone()

            # check to see if the user exists, if not display error message
            if len(matchInput_username) < 1:
                session['attemptError'] = 'This user does not exist, Please register the account and try again.'
                return redirect(url_for('showLogin'))
            
            # displays message upon successful login 
            elif len(matchInput_username) == 1:
                session['attemptSuccess'] = 'Login Success!'
                # stores the vendor's user_name in the session
                flask_session['user_data'] = login_session.USER_NAME
                return redirect(url_for('showVendor'))

 
        else:
            invalid = "This username or password is invalid, please try again."
            return render_template('/login.html', invalid=invalid)


# ------------------------------------------------ End of Login ----------------------------------------------------------------



# -- Start of Log out --








# -- End of log out --




# ------------------------------------------------ Start of Accounts ------------------------------------------------------------

# this is temporary, Jaiden you can delete whatever you need I'm just doing this to see the page and make sure the login function works
@app.route('/accounts')
def showUser():
    return render_template('/my_account.html')

# ------------------------------------------------ End of Accounts --------------------------------------------------------------





# ------------------------------------------------ Start of Admin ------------------------------------------------------------

# temporary view of admin
@app.route('/admin')
def showAdmin():
    return render_template('/admin.html')

# ------------------------------------------------ End of Admin --------------------------------------------------------------




# ------------------------------------------------ Start of Product ------------------------------------------------------------













# ------------------------------------------------ End of Product ------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)

