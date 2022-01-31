from flask import Flask, render_template, escape

app = Flask(__name__)

@app.route('/')
def load_home_page():
    return render_template('homepage.html')

@app.route('/catalog')
def load_catalog():
    return render_template('catalog.html')

@app.route('/about')
def load_about():
    return render_template('about.html')

@app.route('/contacts')
def load_contacts():
    return render_template('contacts.html')

@app.route('/product/<number>')
def load_product(number):
    return render_template(f'product_{escape(number)}.html')

if __name__ == '__main__':
    app.run(debug=True)