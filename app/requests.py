from flask import Flask, render_template, escape, request, session, flash, redirect, url_for, make_response
from models import *
from app import app, db
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        try:
            if Users.query.filter_by(login=login).one().validate(password):
                session['login'] = login
                flash(f'Welcome back, {login}', 'success')
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


@app.route('/shopcart')
def shopcart():
    if session.get('login'):
        u = session.get('login')
        items = Shopping_cart.query.filter_by(customer_id=Users.query.filter_by(login=u).one().id)
        ls = []
        s = 0
        for item in items:
            t = Items.query.filter_by(id=item.item_id).one()
            ls.append(ShopcartList(name=t.name, price=t.price, ttl_price=t.price * item.count, count=item.count, id=item.item_id))
            s += t.price * item.count
        return render_template('shopcart.html', items=ls, ttl_order_price=s)
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


if __name__ == '__main__':
    app.run(debug=True)
