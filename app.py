import os
import psycopg2
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Library_management',
                            user= os.environ['postgres'],
                            password= os.environ['appaamma'])
    return conn

db = SQLAlchemy()

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()