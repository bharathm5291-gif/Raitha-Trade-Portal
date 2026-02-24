# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raitha_trade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(15))

with app.app_context():
    db.create_all()

# Raitha Trade Portal - Karnataka Edition
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .kn-header { 
            background: linear-gradient(to bottom, #ffff00 50%, #ff0000 50%); 
            padding: 30px; text-align: center; font-weight: bold;
        }
        .navbar { background: #1b5e20 !important; }
        .card { border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-karnataka { background: #ff0000; color: #ffff00; font-weight: bold; }
    </style>
</head>
<body>
    <div class="kn-header">
        <h1>ರೈತ ಟ್ರೇಡ್ ಪೋರ್ಟಲ್</h1>
        <h3>RAITHA TRADE PORTAL</h3>
        <p>ಕರ್ನಾಟಕದ ರೈತರಿಗಾಗಿ (For Karnataka Farmers)</p>
    </div>

    <nav class="navbar navbar-expand navbar-dark">
        <div class="container justify-content-center">
            <div class="navbar-nav">
                <a class="nav-link" href="/">ಮಾರುಕಟ್ಟೆ (Market)</a>
                <a class="nav-link" href="/add">ಮಾರಾಟ ಮಾಡಿ (Sell)</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if page == 'home' %}
            <div class="row">
                {% for p in products %}
                <div class="col-md-4 mb-3">
                    <div class="card p-3">
                        <h4 class="text-success">{{ p.name }}</h4>
                        <p>📍 {{ p.location }}</p>
                        <h3>₹{{ p.price }}</h3>
                        <a href="https://wa.me/91{{ p.phone }}" class="btn btn-success">WhatsApp Chat</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% elif page == 'add' %}
            <div class="card p-4 mx-auto" style="max-width: 450px;">
                <form action="/add" method="POST">
                    <input type="text" name="name" class="form-control mb-2" placeholder="ಬೆಳೆ ಹೆಸರು (Crop Name)" required>
                    <input type="number" name="price" class="form-control mb-2" placeholder="ಬೆಲೆ (Price)" required>
                    <input type="text" name="location" class="form-control mb-2" placeholder="ಸ್ಥಳ (Location)" required>
                    <input type="text" name="phone" class="form-control mb-2" placeholder="ವಾಟ್ಸಾಪ್ ಸಂಖ್ಯೆ (WhatsApp No)" required>
                    <button type="submit" class="btn btn-karnataka w-100">ಲೈವ್ ಮಾಡಿ (Go Live)</button>
                </form>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    results = Product.query.all()
    return render_template_string(HTML_TEMPLATE, page='home', products=results)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_p = Product(name=request.form['name'], price=request.form['price'], location=request.form['location'], phone=request.form['phone'])
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, page='add')

if __name__ == '__main__':
    app.run(debug=True)