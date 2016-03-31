from flask import Flask, send_file, render_template, redirect, request, session, flash, jsonify
from mysqlconnection import MySQLConnector
import re

from flask.ext.bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = 'ThisIsSecret'

mysql = MySQLConnector('photos_db')

@app.route('/')
def index():       
    if 'all_photos' not in session:
        query = "SELECT * FROM photos"
        all_photos = mysql.fetch(query)
        session['all_photos'] = all_photos
    if 'total_items' not in session:
        session['total_items'] = 0
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/process_registration', methods=['POST'])
def process_registration():
    valid = True
    if request.form['email'] == "" or not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email address")
        valid = False
    query = "SELECT * FROM users WHERE email = '{}'".format( request.form['email'])
    user = mysql.fetch(query)
    if len(user)>0:
        flash('Email already exists')
        valid = False
    if request.form['first_name'] == "" or not request.form["first_name"].isalpha():
        flash("Enter valid First Name")
        valid = False
    if request.form['last_name'] == "" or not request.form["last_name"].isalpha():
        flash("Enter valid Last Name")
        valid = False
    if request.form['password'] == "" or len(request.form["password"]) < 8:
        flash("Password must contain at least 8 characters") 
        valid = False
    if request.form['password'] !=  request.form['password2']:
        flash("passwords must match")
        valid = False 

    if valid == False:
        return redirect('/register')
    else:        
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password'] 
        pw_hash = bcrypt.generate_password_hash(password)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ('{}', '{}', '{}','{}')".format(request.form['first_name'], request.form['last_name'], request.form['email'], pw_hash)
        mysql.run_mysql_query(query)
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
            session['user_id'] = user[0]['id']
            return render_template('/index.html')
        else:
            flash('Invalid user/password combo')
            valid = False
    return redirect('/')  
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')          

@app.route('/category')
def category(): 
    return render_template('category.html')

@app.route('/payment')
def payment(): 
    return render_template('payment.html')

@app.route('/purchase')
def purchase(): 
    return render_template('purchase.html')

@app.route('/display_photo/<id>')
def display_photo(id):
    query = 'SELECT * FROM photos WHERE id="{}"'.format(id)
    photo = mysql.fetch(query)
    return render_template('picture.html', photo = photo[0])  


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact(): 
    return render_template('contact.html')

@app.route('/get_comments/index_json/<id>')
def get_comments(id):
    query = "SELECT comments.comment, users.first_name, DATE_FORMAT(comments.created_at, '%M %d, %Y, %I:%i:%s %p') AS created_at FROM comments JOIN users ON users.id = comments.user_id WHERE comments.photo_id={} ORDER BY created_at DESC".format(id)
    comments = mysql.fetch(query)
    return jsonify(comments=comments)

@app.route('/insert_comment/index_json/<id>', methods=['POST'])
def insert_comment(id):
    query = "INSERT INTO comments (comment, created_at, updated_at, user_id, photo_id) VALUES ('{}', NOW(), NOW(), '{}', '{}')".format(request.form['comment'], session['user_id'], id)
    mysql.run_mysql_query(query)
    query = "SELECT comments.comment, users.first_name, DATE_FORMAT(comments.created_at, '%M %d, %Y, %I:%i:%s %p') AS created_at FROM comments JOIN users ON users.id = comments.user_id WHERE comments.photo_id={} ORDER BY created_at DESC".format(id)
    comments = mysql.fetch(query)
    return jsonify(comments=comments)

@app.route('/add_to_cart/<id>', methods=['POST'])
def add_to_cart(id):
    print id
    if 'cart' not in session:
        session['cart'] = []
        session['cart'].append(id)
    else:
        session['cart'].append(id)
    session['total_items'] = len(session['cart'])
    return redirect ('/category')

app.run(debug=True)






