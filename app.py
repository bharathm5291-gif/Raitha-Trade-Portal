# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This creates the database file automatically
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raitha_trade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model (The "Model")
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)

# Main Home Route (The "Controller")
@app.route('/')
def home():
    query = request.args.get('q', '')
    if query:
        products = Product.query.filter((Product.crop_name.contains(query)) | (Product.location.contains(query))).all()
    else:
        products = Product.query.all()
    # Looks inside the 'templates' folder for index.html
    return render_template('index.html', products=products, query=query)

# Add Crop Route
@app.route('/add', methods=['POST'])
def add_crop():
    new_product = Product(
        crop_name=request.form.get('crop_name'),
        price=request.form.get('price'),
        location=request.form.get('location'),
        contact=request.form.get('contact')
    )
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
