from flask import Flask
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

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=True)
    feedback = db.Column(db.String(500), nullable=True)

db.create_all()
#db.session.add(Items(name='Калибровочный куб 20x20', category_id=1, price=100, description='Простой калибровочный кубик.'))
#db.session.add(Items(name='Кораблик Benchy', category_id=2, price=250, description='Самая популярная модель для печати!'))
#db.session.add(Items(name='Шестеренки в шестеренке', category_id=3, price=400, description='Хороший успокоитель вашей души'))
#db.session.add(Items(name='Голодный кот', category_id=2, price=200, description='Милый пластиковый котик'))
#db.session.add(Items(name='Шкатулка в форме сердца', category_id=3, price=350, description='Храните свои вещи в своем сердце'))
#db.session.add(Items(name='Шкатулка с апертурным механизмом', category_id=3, price=700, description='Храните свои большие вещи в своей большой шкатулке'))
#db.session.add(Items(name='Зажим для упаковок', category_id=3, price=300, description='Вместо узлов - технологичный зажим!'))
#db.session.add(Items(name='Кубический котик', category_id=2, price=175, description='Кубический, но милый)'))
#db.session.add(Items(name='Температурная башня', category_id=1, price=400, description='Её используют для калибровки температуры'))
#db.session.add(Items(name='Vault Boy', category_id=2, price=500, description='War... war never changes...'))
#db.session.add(Items(name='Шкатулка с головоломкой', category_id=3, price=600, description='Сломай свою голову, пока открываешь шкатулочку)'))
#db.session.commit()