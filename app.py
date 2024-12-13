import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Deepak:Deep@k111@192.168.1.107/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    details = db.Column(db.JSON, nullable=False)

# Initialize database
db.create_all()

# Helper function to generate unique asset ID
def generate_asset_id(company_name, asset_no, asset_type):
    return f"{company_name}-{asset_no}-{asset_type}".upper()

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('index'))
        return "Invalid username or password!", 401
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Main page
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    assets = Asset.query.all()
    return render_template('index.html', assets=assets, role=session['role'], username=session['username'])

@app.route('/add_user', methods=['POST'])
def add_user():
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'})

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'})
    return jsonify({'message': 'User not found!'}), 404

@app.route('/add_asset', methods=['POST'])
def add_asset():
    if 'username' not in session:
        return redirect(url_for('login'))

    category = request.form['category']
    data = {
        'Laptop': ['User Name', 'Serial No.', 'Model', 'Ownership', 'Processor', 'Ram', 'Storage', 'OS', 'Asset Tag', 'Barcode', 'Remark'],
        'Mobile': ['Asset Type', 'Ownership', 'User Name', 'Asset Purchase Date', 'Model', 'Serial No.', 'Ram', 'Storage', 'Asset Tag', 'Barcode', 'Remark'],
        'Pocket SSD & Pendrive': ['Asset Type', 'Ownership', 'User Name', 'Model', 'Serial No.', 'Storage', 'Asset Tag', 'Barcode', 'Remark'],
        'Keyboard, Mouse, CPU': ['Asset Type', 'Ownership', 'User Name', 'Model', 'Serial No.', 'Storage', 'Asset Tag', 'Barcode', 'Remark'],
        'Firewall, Router, Switches, Server Rack': ['Asset Type', 'User Name', 'Model', 'Asset Tag', 'Barcode', 'Remark', 'Location'],
        'Printer, Television, Projector': ['Asset Type', 'User Name', 'Model', 'Asset Tag', 'Barcode', 'Remark', 'Location'],
        'Sound System & Podcast Assets': ['Asset Type', 'User Name', 'Model', 'Asset Tag', 'Barcode', 'Remark', 'Location'],
        'Mac & HDMI Connector': ['Asset Type', 'User Name', 'Model', 'Asset Tag', 'Barcode', 'Remark']
    }

    asset_details = {}
    for field in data.get(category, []):
        asset_details[field] = request.form.get(field)

    # Generate unique asset ID
    company_name = "AYANWORKS"
    asset_no = Asset.query.count() + 1
    asset_id = generate_asset_id(company_name, asset_no, category)

    asset = Asset(asset_id=asset_id, category=category, details=asset_details)
    db.session.add(asset)
    db.session.commit()

    return jsonify({'message': 'Asset added successfully!'})

@app.route('/get_assets', methods=['GET'])
def get_assets():
    if 'username' not in session:
        return redirect(url_for('login'))
    assets = Asset.query.all()
    return jsonify([{'id': asset.id, 'asset_id': asset.asset_id, 'category': asset.category, 'details': asset.details} for asset in assets])

@app.route('/delete_asset/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    asset = Asset.query.get(asset_id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return jsonify({'message': 'Asset deleted successfully!'})
    return jsonify({'message': 'Asset not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)