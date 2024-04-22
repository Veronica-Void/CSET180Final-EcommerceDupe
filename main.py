from flask import Flask, render_template, request, redirect, session, url_for #imported flask and other things here
from sqlalchemy import create_engine, text
import hashlib

c_str = "mysql://root:MySQL8090@localhost/ecomm"
engine = create_engine(c_str, echo=True)
connection = engine.connect

app = Flask(__name__)
app.secret_key = 'hola'




@app.route('/')
def home():
    return render_template('/index.html')












if __name__ == '__main__':
    app.run(debug=True)