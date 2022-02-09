from flask import Flask, render_template, escape, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///extrud3r_orm.db'
db = SQLAlchemy(app)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(80), nullable=True)
    house = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    postcode = db.Column(db.String(80), nullable=True)
    flat = db.Column(db.String(80), nullable=True)
    floor = db.Column(db.String(80), nullable=True)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    birthdate = db.Column(db.String(80), nullable=True)
    login = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(80), nullable=True)
    registration_date = db.Column(db.String(80), nullable=True)


class User_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    users = db.relationship('Users',
                            backref=db.backref('user_add', lazy=False))
    address = db.relationship('Address',
                              backref=db.backref('user_add', lazy=False))


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(80), nullable=True)
    photo = db.Column(db.String(80), nullable=True)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(80), nullable=True)
    category = db.relationship('Categories',
                               backref=db.backref('item', lazy=False))


class Shopping_cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    customer = db.relationship('Users',
                            backref=db.backref('shop_cart', lazy=False))
    item = db.relationship('Items',
                              backref=db.backref('shop_cart', lazy=False))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    customer = db.relationship('Users',
                            backref=db.backref('order', lazy=False))
    address = db.relationship('Address',
                              backref=db.backref('order', lazy=False))


class Order_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    price_per_item = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    order = db.relationship('Orders',
                            backref=db.backref('order_ls', lazy=False))
    item = db.relationship('Items',
                              backref=db.backref('order_ls', lazy=False))



@app.route('/')
def load_home_page():
    return render_template('homepage.html')

@app.route('/catalog')
def load_catalog():
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 10e9))
    items = list(filter(lambda x: min_price <= int(x.price) <= max_price, Items.query.all()))
    return render_template('catalog.html', items=items)

@app.route('/about')
def load_about():
    return render_template('about.html')

@app.route('/contacts')
def load_contacts():
    return render_template('contacts.html')

@app.route('/product/<number>')
def load_product(number):
    return render_template(f'product.html', item=Items.query.filter_by(id=int(escape(number))).one())

if __name__ == '__main__':
    app.run(debug=True)