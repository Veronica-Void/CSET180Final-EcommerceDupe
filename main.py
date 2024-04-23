# from flask_mysqldb import MySQL # Gives flask extensions for MySQL making some work easier.
import MySQLdb.cursors # Imports 'cursors' allows you to interect with MySQL database. Also used to execute SQL queries and fetch data from database.
import re # Provide support for regular expressions, searches and manipulates strings, it helps with a lot of tasks like validation.
from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
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
    return redirect(url_for('showLogin'))
# ------------------------------------------------ End of Register ------------------------------------------------------------




# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
# function uses session to display errors when there is a bad login attempt
def showLogin():
    if 'attemptError' in session:
        var = session.pop('attemptError')
    else:
        # setting an empty variable because a null value can't be passed here
        var = ""
    return render_template('/login.html')

@app.route('/login', methods=['POST'])
# taking values from Session and using them as a comparison to allow access
def loginUser():
    with app.app_context():
        Session = sessionmaker(bind=engine)
        session = Session()

    matchInput_username = request.form.get('USER_NAME')
    matchInput_password = request.form.get('PASSWORD')
    hashedMatchInput_password = hash_password(matchInput_password).hexdigest()
    check_match_exists = conn.execute(text(f'SELECT * FROM USER WHERE USER_NAME = \'{matchInput_username}\'')).all()
    acc_type = conn.execute(text('SELECT ACCOUNT_TYPE FROM USER'))
    if len(check_match_exists) < 1:
        session['attemptError'] = "This user does not exist, please try again."
        return redirect(url_for('showLogin'))
    if acc_type == 'Administrator':
        return redirect(url_for('showAdmin'))
    if hashedMatchInput_password == check_match_exists[0][3]:
        return redirect(url_for('showAccount'))
    
    

    # Kishaun's example of login function
        #     if user.acc_type == 'Admin':
        #         admin = session.execute(text('SELECT * FROM admins WHERE email = :email'),
        #                                 {'email': user.email}).fetchone()
        #         flask_session['user_id'] = admin.AdminID  # Store the admins id in the session
        #         return render_template('admin.html')
        #     elif user.acc_type == 'Customer':
        #         customer = session.execute(text('SELECT * FROM customers WHERE email = :email'),
        #                                    {'email': user.email}).fetchone()
        #         flask_session['user_id'] = customer.CustomerID  # Store the student's ID in the session
        #         flask_session['customer_id'] = customer.CustomerID  # Store the student's ID in the session

        #         # Fetch the AccountNumber for the logged-in customer
        #         account_number = get_logged_in_account_number()
        #         flask_session['account_number'] = account_number  # Store the AccountNumber in the session

        #         return render_template('homepage.html')
        # else:
        #     invalid = "Invalid email or password"
        #     return render_template('login.html', invalid=invalid)

# ------------------------------------------------ End of Login ----------------------------------------------------------------







# ------------------------------------------------ Start of Account ------------------------------------------------------------

# this is temporary, Jaiden you can delete whatever you need I'm just doing this to see the page and make sure the login function works
@app.route('/accounts')
def showAccount():
    return render_template('my_account.html')



# ------------------------------------------------ End of Account --------------------------------------------------------------








# ------------------------------------------------ Start of Product ------------------------------------------------------------
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

