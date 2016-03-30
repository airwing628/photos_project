from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re

from flask.ext.bcrypt import Bcrypt


# hello wing and sammy1111. 
# sdafha
#this is wing's addition

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = 'ThisIsSecret'

mysql = MySQLConnector('photos_db')

@app.route('/')
def index():        
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/process_registration', methods=['POST'])
def process_registration():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    email = request.form['email']
    password = request.form['password'] 

    valid = True
    if str(request.form['email']) == "" or not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a proper email address")
        valid = False
    if str(request.form['first_name']) == "" or not request.form["first_name"].isalpha():
        flash("Enter valid First Name")
        valid = False
    if str(request.form['last_name']) == "" or not request.form["last_name"].isalpha():
        flash("Enter valid Last Name")
        valid = False
    if str(request.form['password']) == "" or len(request.form["password"]) < 8:
        flash("Password must contain at least 8 characters") 
        valid = False
    if request.form['password'] !=  request.form['password2']:
        flash("passwords must match")
        valid = False 

    if valid == False:
        return redirect('/register')    
    
    if valid == True:
        pw_hash = bcrypt.generate_password_hash(password)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ('{}', '{}', '{}','{}')".format(request.form['first_name'], request.form['last_name'], request.form['email'], pw_hash)
        mysql.run_mysql_query(query)
        print query
        return redirect('/')


@app.route('/login', methods=['POST'])
def login(): 
    valid = True
    email = request.form['email']
    password = request.form['password'] 
    query = "SELECT * FROM users WHERE email = '{}'".format(email)
    user = mysql.fetch(query)
    if len(user) < 1:
        flash('Invalid user/password combo')
    else: 
        if bcrypt.check_password_hash(user[0]['password'], password):
            session['loggedin'] = True
            session['first_name'] = user[0]['first_name']
            session['email'] = user[0]['email']
            return render_template('/index.html')
        else:
            flash('Incorrect Password')
            valid = False
    return redirect('/')  
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')          

app.run(debug=True)

