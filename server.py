from flask import Flask, send_file, render_template, redirect, request, session, flash, jsonify

from mysqlconnection import MySQLConnector

import re

import stripe

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
    query = "SELECT * FROM users WHERE email = '{}'".format(re.escape(request.form['email']))
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
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ('{}', '{}', '{}','{}')".format(re.escape(first_name), re.escape(request.form['last_name']), re.escape(request.form['email']), pw_hash)
        mysql.run_mysql_query(query)
        query = "SELECT * FROM users WHERE email = '{}'".format(re.escape(email))
        user = mysql.fetch(query)
        session['first_name'] = user[0]['first_name']
        session['email'] = user[0]['email']
        session['user_id'] = user[0]['id']
        return redirect('/')


@app.route('/login', methods=['POST'])
def login(): 
    valid = True
    email = request.form['email']
    password = request.form['password'] 
    query = "SELECT * FROM users WHERE email = '{}'".format(re.escape(email))
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
    session['total_cart'] = []
    if 'cart' not in session:
        total_price = 0
        return render_template('/purchase.html', total_price = total_price)
    if len(session['cart']) == 0:
        cart = "empty"
        total_price = 0
    else:
        cart = "not_empty"      
        for photo in session['cart']:
            query = "SELECT * FROM photos WHERE id = {}".format(photo)
            fetch = mysql.fetch(query)
            session['total_cart'].append(fetch[0])
        total_price = 0
        for i in range(0, len(session['total_cart'])):
            total_price += session['total_cart'][i]['price']
    return render_template('purchase.html', total_price = total_price, cart=cart)

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
    query = "INSERT INTO comments (comment, created_at, updated_at, user_id, photo_id) VALUES ('{}', NOW(), NOW(), '{}', '{}')".format(re.escape(request.form['comment']), session['user_id'], id)
    mysql.run_mysql_query(query)
    query = "SELECT comments.comment, users.first_name, DATE_FORMAT(comments.created_at, '%M %d, %Y, %I:%i:%s %p') AS created_at FROM comments JOIN users ON users.id = comments.user_id WHERE comments.photo_id={} ORDER BY created_at DESC".format(id)
    comments = mysql.fetch(query)
    return jsonify(comments=comments)

@app.route('/add_to_cart/<id>', methods=['POST'])
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
        session['cart'].append(id)
    else:
        session['cart'].append(id)
    session['total_items'] = len(session['cart'])
    return redirect ('/category')

@app.route('/remove_cart_item/<id>')
def remove_cart_item(id):
    session['cart'].remove(id)
    session['total_items'] = len(session['cart'])
    return redirect('/purchase')

@app.route('/process_stripe', methods=['POST'])
def process_stripe():
    print request.form
    print 'in process stripe'
    stripe.api_key = "sk_test_UhKc5Gi7liEBEhQ3Hfs9FvRs"
    # Get the credit card details submitted by the form
    token = request.form['stripeToken']
    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        charge = stripe.Charge.create(
            amount=1000, # amount in cents, again
            currency="usd",
            source=token,
            description="Example charge"
        )
    except stripe.error.CardError, e:
      # The card has been declined
        pass
    return redirect('/process_download')

@app.route('/process_download')
def process_download():
    session['total_items'] = 0
    session['download'] = []
    for photo in session['cart']:
        query = "SELECT * FROM photos WHERE id = {}".format(photo)
        fetch = mysql.fetch(query)
        session['download'].append(fetch[0])
    session.pop('cart')
    return redirect('/download')

@app.route('/download')
def download():
    return render_template('download.html', downloads=session['download'])

app.run(debug=True)






