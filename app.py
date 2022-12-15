import os 
import sqlite3
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, validators, StringField


app = Flask(__name__)

#def get_db_connection():
    #conn = psycopg2.connect(host='localhost',
                            #user= os.environ['postgres'],
                            #port= os.environ['5432'],
                            #password= os.environ['appaamma'])
   # return conn
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
db = SQLAlchemy()

# Route for home page
@app.route('/')
def index():
    return render_template('home.html')

#Route to Reader page
@app.route('/reader')
def reader():
    return render_template('reader.html')

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

#class AddReader(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    phone = StringField('Phone', [validators.length(min=6, max=50)])


# Add Reader
@app.route('/add_reader', methods=['GET', 'POST'])
def add_reader():
    conn = get_db_connection()
    reader = conn.execute("SELECT * FROM Reader").fetchall()
    conn.close
    return render_template('add_reader.html', reader=reader)

#class AddDocument(Form):
    title = StringField('Title', [validators.Length(min=1, max=50)])
    publisher = StringField('Publisher', [validators.length(min=6, max=50)])


# Add document
@app.route('/addDocument', methods=['GET', 'POST'])
def insertDocument():
    conn = get_db_connection()
    title = request.form['title']
    pdate = request.form['pdate']
    pid = request.form['pid']
    if (title != "" and pdate!= "" and pid != ""):
        conn.execute(
            "INSERT INTO document (TITLE, PDATE) VALUES (?,?)", (title, pdate))
        conn.commit()
    conn.close()
    flash("Document added!")
    return redirect('/show_document.html')


# print document
@app.route('/show_document', methods=['GET', 'POST'])
def show_document():
    conn = get_db_connection()
    document = conn.execute("SELECT * FROM document").fetchall()
    conn.close()
    return render_template('show_Document.html', document=document)



@app.route('/addReader', methods=['GET', 'POST'])
def insertReader():
    conn = get_db_connection()
    rname = request.form['reader-name']
    raddress = request.form['reader-address']
    rphone = request.form['reader-phoneno']

    if (rname != "" and raddress != "" and rphone != ""):
        conn.execute(
            "INSERT INTO readers (RNAME, RADDRESS, PHONE_NO) VALUES (?, ?, ?)", (rname, raddress, rphone))
        conn.commit()
    conn.close()
    flash("User added successfully!!!")
    return redirect('/adminLogin/addReader')

   





if __name__ == '__main__':
    app.debug = True
    app.run()