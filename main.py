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

