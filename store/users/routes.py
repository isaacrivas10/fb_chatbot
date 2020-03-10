
from flask import Blueprint, redirect, flash, url_for, request, render_template
from flask_login import login_user, current_user, logout_user
from store import bcrypt, db, handler
from store.users.forms import LoginForm, RegistrationForm
from store.models.user import User

users= Blueprint('users', __name__)

@users.route("/forms/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Inicio de sesion fallido. Por favor revisar email y contraseña.')
    return render_template('login.html', title='Login', form=form)

@users.route("/forms/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= RegistrationForm()
    ip= request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(ip)
    if form.validate_on_submit():
        hashed_pwd= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(first_name= form.firstName.data,
                    last_name= form.lastName.data,
                    email= form.email.data,
                    password= hashed_pwd,
                    phone_number= form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido creada con exito. Por favor inicia sesión.')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, geo=handler.getDetails(ip))

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')