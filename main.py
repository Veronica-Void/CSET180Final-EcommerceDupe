# i keep getting a yellow error whenever I uncomment this import - Vee
# from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.

import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.

from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
# from flask import session as session

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
@app.route('/register', methods=['POST'])
def registerUser():
    # grabbing the values that the user puts into the sign up form
    user_name = request.form.get('USER_NAME')
    name = request.form.get('NAME')
    email = request.form.get('EMAIL')
    password = request.form.get('PASSWORD')
    acc_type = request.form.get('ACCOUNT_TYPE')
    # hashing the password value
    hashed_password = hash_password(password).hexdigest()

    # inserting values including hashed password into the database
    conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', \'{acc_type}\')'))
    conn.commit() #extra layer of protection

    # I NEED TO MAKE A CHECK FOR IF THE USER ALREADY EXISTS AND DISPLAY ERROR MESSAGE 

    return redirect(url_for('showLogin'))


    

# ------------------------------------------------ End of Register ------------------------------------------------------------




# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
# function uses session to display errors when there is a bad login attempt
def showLogin():
  return render_template('/login.html')


 

@app.route('/login', methods=['POST'])
# actual login function 
# taking values from Session and using them as a comparison to allow access
def loginUser():
  
    # was trying to store these values in session - Vee
    session['login_username'] = request.form.get('USER_NAME')
    session['login_email'] = request.form.get('EMAIL')
    session['login_password'] = request.form.get('PASSWORD')

    # this is how I was grabbing values from the form to later compare them -Vee
    login_username = request.form.get('USER_NAME')
    login_email = request.form.get('EMAIL')
    login_password = request.form.get('PASSWORD')
    hashed_login_password = hash_password(login_password).hexdigest() #this should probably stay because you need to match up the password from the login form with the password that's already in the db (from the sign up form)


    # selects everything from the db using the username or email that comes from the login form
    checkif_userExists = conn.execute(text(f'SELECT * FROM USER WHERE USER_NAME = \'{login_username}\' OR EMAIL = \'{login_email}\''))

    return render_template('index.html') # just returning the home page because something needs to be returned from the function

    

# ------------------------------------------------ End of Login ----------------------------------------------------------------



# -- Start of Log out --








# -- End of log out --




# ------------------------------------------------ Start of User Accounts ------------------------------------------------------------

# this is temporary, Jaiden you can delete whatever you need I'm just doing this to see the page and make sure the login function works
@app.route('/accounts')
def showUser():
    user_data = 'ehehehehe'
    return render_template('/my_account.html', user_data=user_data)

# ------------------------------------------------ End of User Accounts --------------------------------------------------------------





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

