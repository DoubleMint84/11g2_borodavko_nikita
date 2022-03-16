from flask import Flask, render_template, escape, request, session, flash, redirect, url_for, make_response
from models import *
from app import app, db
import sqlalchemy
from datetime import datetime, timedelta


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

@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
    if session.get('login') == name:
        if (u := Users.query.filter_by(login=login)) is not None:
            if request.method == 'POST':
                u = u.one()
                old = request.form.get('old_password')
                new = request.form.get('new_password')
                if old == new:
                    flash('Новый пароль тот же, что и старый', 'warning')
                elif u.validate(old):
                    u.set_password(new)
                    flash('Пароль изменен', 'success')
                    db.session.add(u)
                    db.session.commit()
            return render_template('profile.html', user=u)
    flash('Please authenticate', 'warning')
    return redirect(url_for('login'), code=301)


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


@app.route('/product/<number>')
def load_product(number):
    return render_template(f'product.html', item=Items.query.filter_by(id=int(escape(number))).one())


if __name__ == '__main__':
    app.run(debug=True)
