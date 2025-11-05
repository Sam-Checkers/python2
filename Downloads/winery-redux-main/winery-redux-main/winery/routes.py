from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from winery.forms import RegistrationForm, LoginForm, UpdateAccountForm
from winery.models import User, check_password_hash, db, wine_schema, wine_schema, Wine, WineUser
from flask_login import login_user, current_user, logout_user, login_required 
from winery import app
from sqlalchemy.exc import IntegrityError

@app.route("/")
@app.route("/brewery")
def brewery():
    wines = Wine.query.all()
    return render_template('brewery.html', title='brewery', wines=wines)

@app.route("/containers")
def containers():
    return render_template('containers.html', title='containers')

def wines():
    items = Wine.query.all()
    return render_template('home.html', items=items)

@app.route('/wines')
def display_wines():
    wines = Wine.query.all()
    return render_template('wines.html', wines=wines)

@app.route('/add_to_shelf/<int:wine_id>')
@login_required
def add_to_shelf(wine_id):
    user_id = current_user.id
    item_id = wine_id
    try:
        user = User.query.get(user_id)
        item = Wine.query.get(item_id)
        user.wines.append(item)
        db.session.commit()
        print('Success!')
    except:
        print('Already on Your Shelf')
    return redirect(url_for('brewery'))

@app.route('/shelf/<int:user_id>')
def shelf(user_id):
    user = User.query.get(user_id)
    shelf_items = user.shelf
    return render_template('home.html', user=user, shelf_items=shelf_items)

@app.route('/remove_from_shelf/<int:wine_id>')
def remove_from_shelf(wine_id):
    user_id = current_user.id
    item_id = wine_id

    user = User.query.get(user_id)
    item = Wine.query.get(item_id)
    user.wines.remove(item)
    db.session.commit()
    return redirect(url_for('home'))
    
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first.data
        last_name = form.last.data
        email = form.email.data
        password = form.password.data
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user = User(first_name, last_name, username, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email,password)
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('Success')
            return redirect(url_for('home'))
        else:
            flash('Check email and password')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/user_info/<int:user_id>", methods=['GET'])
def get_user_info(user_id):
    user = User.query.get(user_id)
    if user:
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return jsonify(user_info), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
@app.route("/get_all_wines", methods=['GET'])
def get_all_wines():
    wines = Wine.query.all()
    wine_list = []
    for wine in wines:
        wine_info = {
            'wine_id': wine.wine_id,
            'name': wine.name,
            'type': wine.type,
            'region': wine.region
        }
        wine_list.append(wine_info)
    return jsonify(wine_list), 200

@app.route("/wine/<int:wine_id>", methods=['GET'])
def get_wine(wine_id):
    wine = Wine.query.get(wine_id)
    if wine:
        wine_info = {
            'wine_id': wine.wine_id,
            'name': wine.name,
            'type': wine.type,
            'region': wine.region
        }
        return jsonify(wine_info), 200
    else:
        return jsonify({'error': 'Wine not found'}), 404
    
@app.route("/update_wine/<int:wine_id>", methods=['PUT'])
def update_wine(wine_id):
    wine = Wine.query.get(wine_id)
    if wine:
        data = request.get_json()
        wine.name = data.get('name', wine.name)
        wine.type = data.get('type', wine.type)
        wine.region = data.get('region', wine.region)
        db.session.commit()
        return jsonify({'message': 'Wine updated successfully'}), 200
    else:
        return jsonify({'error': 'Wine not found'}), 404

@app.route("/add_wine", methods=['POST'])
def add_wine():
    data = request.get_json()
    new_wine = Wine(
        name=data['name'],
        type=data['type'],
        region=data['region']
    )
    try:
        db.session.add(new_wine)
        db.session.commit()
        return jsonify({'message': 'Wine added successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add wine. IntegrityError: {}'.format(str(e))}), 400

@app.route("/delete_wine/<int:wine_id>", methods=['DELETE'])
def delete_wine(wine_id):
    wine = Wine.query.get(wine_id)
    if wine:
        db.session.delete(wine)
        db.session.commit()
        return jsonify({'message': 'Wine deleted successfully'}), 200
    else:
        return jsonify({'error': 'Wine not found'}), 404

from flask import Flask, send_from_directory, abort
import os

@app.route('/images/<image_name>')
def get_image(image_name):
    """
    Serve an image from the static/images directory based on its name.
    
    Args:
        image_name (str): The name of the image file to retrieve
        
    Returns:
        The requested image file or 404 if not found
    """
    # Print debugging information
    print(f"Request for image: {image_name}")
    
    # Get the absolute path to the images directory
    # Option 1: If the notebook is in the same directory level as the winery folder
    images_dir = os.path.join(os.getcwd(), 'winery', 'static', 'images')
    
    # Option 2: If the winery folder is the root directory
    # images_dir = os.path.join('static', 'images')
    
    # Print the directory we're looking in
    print(f"Looking for image in: {images_dir}")
    
    # Check if the directory exists
    if not os.path.exists(images_dir):
        print(f"Directory does not exist: {images_dir}")
        return f"Error: Images directory not found at {images_dir}", 404
    
    # Check if the file exists
    full_path = os.path.join(images_dir, image_name)
    if not os.path.exists(full_path):
        print(f"Image not found: {full_path}")
        return f"Error: Image {image_name} not found", 404
    
    print(f"Found image at: {full_path}")
    # Return the requested image
    return send_from_directory(images_dir, image_name)

# Alternative route that might work better with your directory structure
@app.route('/winery/static/images/<image_name>')
def get_image_alt(image_name):
    """Alternative route that matches the directory structure directly"""
    base_dir = os.getcwd()  # Get current working directory
    return send_from_directory(os.path.join(base_dir, 'winery', 'static', 'images'), image_name)
    
from flask import jsonify
from sqlalchemy import text
from winery import app, root_db

@app.route('/test-db')
def test_db():
    try:
        # Use text() to create an executable SQL expression
        result = root_db.session.execute(text("SELECT version()")).scalar()
        return f"Connected to CockroachDB: {result}"
    except Exception as e:
        return f"Error connecting to database: {str(e)}"