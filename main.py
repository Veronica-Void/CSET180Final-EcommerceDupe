from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
from sqlalchemy import create_engine, text
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
    # hashing the password value
    hashed_password = hash_password(password).hexdigest()
    # inserting values including hashed password into the database
    conn.execute(text(f'INSERT INTO USER (USER_NAME, NAME, EMAIL, PASSWORD, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{hashed_password}\', "customer")'))
    conn.commit() #extra layer of protection
    return redirect(url_for('showLogin'))
# ------------------------------------------------ End of Register ------------------------------------------------------------




# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
def showLogin():
    return render_template('/login.html')

@app.route('/login', methods=['POST'])
def loginUser():
    matchInput_username = request.form.get('USER_NAME')
    matchInput_password = request.form.get('PASSWORD')
    hashedMatchInput_password = hash_password(matchInput_password).hexdigest()
    check_match_exists = conn.execute(text(f'SELECT * FROM USER WHERE PASSWORD = \'{matchInput_username}\''))
    if len(check_match_exists) < 1:
        session['attemptError'] = "This user does not exist, please try again."
        return redirect(url_for('showLogin'))
    if matchInput_password == 'Admin11':
        return redirect(url_for('showAdmin'))
    if hashedMatchInput_password == check_match_exists[0][4]:
        return redirect(url_for('showCustomerAccount'))

# ------------------------------------------------ End of Login ------------------------------------------------------------






if __name__ == '__main__':
    app.run(debug=True)