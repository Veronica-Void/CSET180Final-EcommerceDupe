# from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.
import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.
from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import hashlib

c_str = "mysql://root:MySQL8090@localhost/ecomm"
engine = create_engine(c_str, echo=True)

conn = engine.connect()

app = Flask(__name__)
app.secret_key = 'hola'

# I honestly don't know what this is, my team member showed it to me but im still confused :) is this starting the session? yo no se shawty.
# with app.app_context():
#     Session = sessionmaker(bind=engine) 
#     session = Session()


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
    conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', "customer")'))
    conn.commit() #extra layer of protection
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
    return render_template('/login.html')


@app.route('/login', methods=['POST'])
# taking values from Session and using them as a comparison to allow access
def loginUser():


    matchInput_username = request.form.get('USER_NAME')
    matchInput_password = request.form.get('PASSWORD')
    # acc_type = conn.execute(text(f'SELECT ACCOUNT_TYPE FROM USER')).all()

    hashedMatchInput_password = hash_password(matchInput_password).hexdigest()
    check_match_exists = conn.execute(text(f'SELECT USER_NAME, PASSWORD FROM USER WHERE USER_NAME = \'{matchInput_username}\'')).all()

    # checking if user exists
    if len(check_match_exists) < 1:
        session['attemptError'] = "This user does not exist, please try again."
        return redirect(url_for('showLogin'))
    # gives successful login message
    elif len(check_match_exists) == 1:
        session['attemptSuccess'] = "Login Success!"
        return redirect(url_for('showUser_Account'))
    
    # checking if login = Admin by username & password
    elif matchInput_username == 'smithJ_2024' and matchInput_password == 'Admin11':
        return redirect(url_for('showAdmin'))
    # checking if username and hashed password match the database
    elif hashedMatchInput_password == check_match_exists[0][3] and matchInput_username == check_match_exists[0][0]:
        return redirect(url_for('showUser_Account'))
    
    # takes customer to their specific account 
    # elif acc_type == 'customer':
    #     return redirect(url_for('showUser_Account'))
    
    # if user account not created at all then it will just take them to where they can buy items
    else:
        return redirect(url_for('display_products'))

# ------------------------------------------------ End of Login ----------------------------------------------------------------







# ------------------------------------------------ Start of Accounts ------------------------------------------------------------

# this is temporary, Jaiden you can delete whatever you need I'm just doing this to see the page and make sure the login function works
@app.route('/accounts')
def showUser_Account():
    return render_template('/my_account.html')

# ------------------------------------------------ End of Accounts --------------------------------------------------------------



# ------------------------------------------------ Start of Admin ------------------------------------------------------------

# temporary view of admin
@app.route('/admin')
def showAdmin():
    return render_template('/admin.html')

# ------------------------------------------------ End of Admin --------------------------------------------------------------




# ------------------------------------------------ Start of Product ------------------------------------------------------------

# keep or delete? 
# def product():
#     products = product.query.all()
#     return render_template('product.html', products=products)


# @app.route('/product/<pid>')
# def product_detail(pid):
#     product = product.query.filter_by(PID=pid).first()
#     return render_template('product_detail.html', product=product)
# ------------------------------------------------ End of Product ------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)

