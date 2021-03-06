import re
from flask import Flask, render_template, escape, request, session, flash, redirect, url_for, make_response
from app.models import *
from app.app import app, db
import sqlalchemy
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class ShopcartList:
    name: str
    price: int
    ttl_price: int
    count: int
    id: int


@dataclass
class ItemList:
    name: str
    count: int
    price: int
    total_price: int

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if session.get('login'):
        return redirect(url_for('load_home_page'), code=301)
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        birthdate = request.form.get('birthdate')
        login = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if name == '' or surname == '' or birthdate == '' or login == '' or password1 == '' or password2 == '':
            flash('Заполните все поля', 'warning')
            return render_template('registration.html')
        if len(birthdate) != 10 or re.match(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])', birthdate) is None:
            flash('Некорректная дата рождения', 'warning')
            return render_template('registration.html')
        if password1 != password2:
            flash('Пароли не совпадают', 'warning')
            return render_template('registration.html')
        try:
            Users.query.filter_by(login=login).one()
            flash("Такой логин уже зарегистрирован, выберите другой логин", "warning")
            return render_template('registration.html')
        except sqlalchemy.exc.NoResultFound as e:
            print(e, e.args)
            user = Users(name, surname, birthdate, login, password1)
            db.session.add(user)
            db.session.commit()
            session["login"] = login
            flash(f"Добро пожаловать, {name}!", "success")
            return redirect(url_for("load_home_page"))
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        try:
            if Users.query.filter_by(login=login).one().validate(password):
                session['login'] = login
                flash(f'С возвращением, {Users.query.filter_by(login=login).one().name}!', 'success')
                return redirect(url_for('load_home_page'), code=301)
            flash('Wrong login or password', 'warning')
        except sqlalchemy.exc.NoResultFound:
            flash('Wrong login or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('login'):
        session.pop('login')
    return redirect('/', code=302)


@app.route('/profile/<login>', methods=['GET', 'POST'])
def profile(login):
    if session.get('login') == login:
        if (u := Users.query.filter_by(login=login)) is not None:
            u = u.one()
            if request.method == 'POST':
                old = request.form.get('old_password')
                new = request.form.get('new_password')
                if old == new:
                    flash('Новый пароль тот же, что и старый', 'warning')
                elif u.validate(old):
                    u.set_password(new)
                    flash('Пароль изменен', 'success')
                    db.session.add(u)
                    db.session.commit()
            #print(u.name)
            addresses = User_address.query.filter_by(customer_id=u.id).all()
            #print(addresses[0].customer_id)
            ls = []
            for i in addresses:
                ls.append(Address.query.filter_by(id=i.address_id).one())
            return render_template('profile.html', user=u, address=ls)
    if session.get('login'):
        flash('Access denied', 'warning')
        return redirect(url_for('profile', login=session.get('login')))
    flash('Please authenticate', 'warning')
    return redirect(url_for('login'))


@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if (login := session.get('login')):
        if (u := Users.query.filter_by(login=login)) is not None:
            u = u.one()
            if request.method == 'POST':
                country = request.form.get('country')
                city = request.form.get('city')
                street = request.form.get('street')
                house = request.form.get('house')
                floor = request.form.get('floor')
                flat = request.form.get('flat')
                if country == '' or city == '' or street == '' or house == '' or floor == '' or flat == '':
                    flash('Заполните все поля', 'warning')
                    return render_template('add_address.html')
                t = Address(country=country, city=city, street=street, house=house, floor=floor, flat=flat)
                db.session.add(t)
                db.session.commit()
                db.session.add(User_address(customer_id=u.id, address_id=int(Address.query.all()[-1].id)))
                db.session.commit()
                flash('Адрес успешно добавлен', 'success')
                return redirect(url_for('profile', login=login))
            return render_template('add_address.html')
    flash('Please authenticate', 'warning')
    return redirect(url_for('login'))


@app.route('/shopcart', methods=['GET', 'POST'])
def shopcart():
    if (u := session.get('login')):
        if request.method == 'POST':
            try:
                addr_id = int(request.form['options'])
                user_id = Users.query.filter_by(login=u).one().id
                items = Shopping_cart.query.filter_by(customer_id=user_id).all()
                ttl = 0
                for i in items:
                    t = Items.query.filter_by(id=i.item_id).one()
                    ttl += i.count * t.price
                order = Orders(customer_id=user_id, date=str(datetime.now())[:16], total=ttl, state=0, address_id=addr_id)
                db.session.add(order)
                db.session.flush()
                order_id = order.id
                for i in items:
                    t = Items.query.filter_by(id=i.item_id).one()
                    db.session.add(Order_list(order_id=order_id, item_id=i.item_id, price_per_item=t.price, count=i.count))
                db.session.flush()
                Shopping_cart.query.filter_by(customer_id=user_id).delete()
                db.session.commit()
                flash(f'Заказ №{order_id} успешно создан', 'success')
                return redirect(url_for('my_orders'))
            except:
                flash('Выберите адрес доставки', 'warning')
        items = Shopping_cart.query.filter_by(customer_id=Users.query.filter_by(login=u).one().id)
        ls = []
        s = 0
        for item in items:
            t = Items.query.filter_by(id=item.item_id).one()
            ls.append(ShopcartList(name=t.name, price=t.price, ttl_price=t.price * item.count, count=item.count, id=item.item_id))
            s += t.price * item.count
        user = Users.query.filter_by(login=u).one()
        addresses = User_address.query.filter_by(customer_id=user.id).all()
        # print(addresses[0].customer_id)
        addr = []
        for i in addresses:
            addr.append(Address.query.filter_by(id=i.address_id).one())
        return render_template('shopcart.html', items=ls, ttl_order_price=s, address=addr)
    else:
        flash('Please authenticate', 'warning')
        return redirect(url_for('login'))


@app.route('/')
def load_home_page():
    feedback_list = Feedback.query.all()
    resp = make_response(render_template('homepage.html', feedback=feedback_list))
    if not request.cookies.get('test'):
        resp.set_cookie('test', 'testvalue', expires=datetime.now() + timedelta(minutes=30))
    return resp


@app.route('/catalog')
def load_catalog():
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 10e9))
    items = list(filter(lambda x: min_price <= int(x.price) <= max_price, Items.query.all()))
    return render_template('catalog.html', items=items)


@app.route('/about')
def load_about():
    return render_template('about.html', feedback=Feedback.query.all())


@app.route('/contacts', methods=['GET', 'POST'])
def load_contacts():
    if request.method == 'POST':
        login = request.form.get('login')
        text = request.form.get('feedback')
        if login != '' and text != '':
            db.session.add(Feedback(login=login, feedback=text))
            db.session.commit()
    feedback_list = Feedback.query.all()
    return render_template('contacts.html', feedback=feedback_list)


@app.route('/product/<number>/buy_one')
def buy_product(number):
    #print('buy', number)
    item_id = int(escape(number))
    if session.get('login'):
        customer_id = int(Users.query.filter_by(login=session.get('login')).one().id)
        cart = Shopping_cart.query.filter_by(item_id=item_id, customer_id=customer_id)
        if len(list(cart)) == 0:
            db.session.add(Shopping_cart(customer_id=customer_id, item_id=item_id, count=1))
        else:
            cart = cart.one()
            cart.increment()
        db.session.commit()
    else:
        flash('Please authenticate', 'warning')
        return redirect(url_for('login'))
    return redirect(url_for('load_product', number=number))


@app.route('/product/<number>/del_item')
def del_product(number):
    item_id = int(escape(number))
    if session.get('login'):
        customer_id = int(Users.query.filter_by(login=session.get('login')).one().id)
        cart = Shopping_cart.query.filter_by(item_id=item_id, customer_id=customer_id)
        cart = cart.one()
        db.session.delete(cart)
        db.session.commit()
    else:
        flash('Please authenticate', 'warning')
        return redirect(url_for('login'))
    return redirect(url_for('load_product', number=number))


@app.route('/shopcart/<number>/del_item')
def del_item_shopcart(number):
    item_id = int(escape(number))
    if session.get('login'):
        customer_id = int(Users.query.filter_by(login=session.get('login')).one().id)
        cart = Shopping_cart.query.filter_by(item_id=item_id, customer_id=customer_id)
        cart = cart.one()
        db.session.delete(cart)
        db.session.commit()
    else:
        flash('Please authenticate', 'warning')
        return redirect(url_for('login'))
    return redirect(url_for('shopcart'))


@app.route('/product/<number>')
def load_product(number):
    #print(number)
    item_id = int(escape(number))
    item = Items.query.filter_by(id=item_id).one()
    if session.get('login'):
        customer_id = int(Users.query.filter_by(login=session.get('login')).one().id)
        cart = Shopping_cart.query.filter_by(item_id=item_id, customer_id=customer_id)
        if len(list(cart)) == 0:
            count = 0
        else:
            count = int(cart.one().count)
    else:
        count = 0
    return render_template(f'product.html', item=item, count=count)


@app.route('/my_orders')
def my_orders():
    if (login := session.get('login')):
        if (u := Users.query.filter_by(login=login)) is not None:
            u = u.one()
            orders = Orders.query.filter_by(customer_id=u.id).all()
            state = []
            address = []
            items = []
            for order in orders:
                if order.state == 0:
                    state.append('В обработке')
                address.append(Address.query.filter_by(id=order.address_id).one())
                tmp = []
                for i in Order_list.query.filter_by(order_id=order.id).all():
                    item = Items.query.filter_by(id=i.item_id).one()
                    tmp.append(ItemList(name=item.name, count=i.count, price=i.price_per_item, total_price=i.count * i.price_per_item))
                items.append(tmp)
            return render_template('my_orders.html', orders=orders, state=state, address=address, items=items)
    flash('Please authenticate', 'warning')
    return redirect(url_for('login'))
