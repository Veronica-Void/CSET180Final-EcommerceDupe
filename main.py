from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
from sqlalchemy import create_engine, text
import hashlib

c_str = "mysql://root:MySQL8090@localhost/ecomm"
engine = create_engine(c_str, echo=True)
conn = engine.connect

app = Flask(__name__)
app.secret_key = 'hola'

@app.route('/')
def home():
    return render_template('/index.html')

# ------------------------------------------------ Start of Register ------------------------------------------------------------
def hash_password(inputpw):
    return hashlib.sha3_256(inputpw.encode())


@app.route('/register', methods=['GET'])
def showRegister():
    return render_template('/register.html')


@app.route('/register', methods=['POST'])
def registerUser():
    user_name = request.form.get('USER_NAME')
    name = request.form.get('NAME')
    email = request.form.get('EMAIL')
    password = request.form.get('PASSWORD')
    hashed_password = hash_password(password).hexdigest()
    conn.execute(text(f'INSERT INTO `USER` (USER_NAME, `NAME`, EMAIL, `PASSWORD`, ACCOUNT_TYPE) VALUES (\'{user_name}\', \'{name}\',\'{email}\',\'{password}\'), ""'))
    conn.commit
    return redirect(url_for('showLogin'))
# ------------------------------------------------ End of Register ------------------------------------------------------------




# ------------------------------------------------ Start of Login ------------------------------------------------------------
@app.route('/login', methods=['GET'])
def showLogin():
    return render_template('/login.html')

# @app.route('/login', methods=['POST'])
# def loginUser():
# ------------------------------------------------ End of Login ------------------------------------------------------------






if __name__ == '__main__':
    app.run(debug=True)