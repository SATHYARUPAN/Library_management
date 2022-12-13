import os
import psycopg2
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, validators, StringField


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Library_management',
                            user= os.environ['postgres'],
                            password= os.environ['appaamma'])
    return conn

db = SQLAlchemy()

# Route for home page
@app.route('/')
def index():
    return render_template('home.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('admin.html')
    return render_template('login.html', error=error)

class AddReader(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.length(min=6, max=50)])


# Add Reader
@app.route('/add_reader', methods=['GET', 'POST'])
def add_reader():
    # Get form data from request
    form = AddReader(request.form)
    return render_template('add_reader.html', form=form)




if __name__ == '__main__':
    app.debug = True
    app.run()