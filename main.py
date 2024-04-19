from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'secret_key'


conn_str = "mysql://root:cyber241@localhost/170final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()




