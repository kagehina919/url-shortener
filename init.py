from flask import Flask, render_template, request, redirect, flash, send_from_directory
from db_connect import connection
from shorten import shorten_url
from wtforms import Form, TextField, PasswordField
from passlib.handlers.sha2_crypt import sha256_crypt
import os

app = Flask(__name__)
default = "true"

@app.route('/')
def main():
    return render_template("main.html")

class registerationForm(Form):
    username = TextField('username')
    email=TextField('email')
    password=PasswordField('password')


@app.route('/random')
def dae():
    return render_template("urls.html")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form= registerationForm(request.form)
    if request.method == 'POST' and form.validate:
        username = form.username.data
        email=form.email.data
        password=form.password.data
        c, conn= connection()
        user = "INSERT INTO register (username, email, password) VALUES ('%s', '%s', '%s')" % (username, email, password)
        c.execute(user)
        conn.commit()
        return render_template("login.html")
    return render_template("register.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        c, conn = connection()
        username_form = request.form['username']
        password_form = request.form['password']
        c.execute("SELECT username FROM register WHERE username = ('%s')" % username_form)
        c.execute("SELECT password FROM register WHERE username = ('%s')" % username_form)
        passw = c.fetchone()
        print(passw[0])
        print(password_form)
        if password_form == passw[0]:
            return render_template("urls.html")
    else:
        flash("invalid credentials!!")
        return render_template("login.html")

@app.route('/shortener/', methods=['GET', 'POST'])
def shorten():
    long = request.form.get('long_url')
    c, conn = connection()
    insert_command = "INSERT INTO urls (long_url, short_url) VALUES ('%s', '%s')" % (long, default)
    status = c.execute(insert_command)
    conn.commit()

    c, conn = connection()
    get_id_command = "SELECT ID FROM urls WHERE long_url = '" + long + "'"
    c.execute(get_id_command)
    id = c.fetchone()
    print(id[0])

    short = shorten_url(id[0])
    c.execute("""
       UPDATE urls
       SET short_url = %s
       WHERE id = %s
    """, (short, id))
    conn.commit()
    return short

@app.route('/short-url/')
def url():
    return render_template("urls.html")

@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<string:short_url>/')
def return_long_url(short_url):
    c, conn= connection()
    long = "SELECT long_url FROM urls WHERE short_url = '" + short_url + "'"
    print(long)
    c.execute(long)
    lon = c.fetchone()
    print(lon[0])
    return redirect(lon[0])

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True, host="0.0.0.0")