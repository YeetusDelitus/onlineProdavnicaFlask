from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json

auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('stefannemanja')
newUserGlobal = User()

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email is already in use.', category='error')
        elif password != password2:
            flash('Passwords do not match', category='error')
        elif len(email) < 4:
            flash('Email needs to be at least four characters long.', category='error')
        elif len(password) < 7:
            flash('Password needs to be at least seven characters long.', category='error')
        else:
            global newUserGlobal
            newUser = User(email=email, firstName=firstName, password=generate_password_hash(password, method='sha256'), admin=True, banned=False)
            newUserGlobal = newUser
            token = s.dumps(email)
            msg = Message('Confirm Email', sender='throwaway82678@gmail.com', recipients=[email])
            link = url_for('auth.verify', token=token, _external=True)
            msg.body = f'Your link is {link}'
            mail.send(msg)

            return render_template('verification.html', user=current_user, state='wait')

    return render_template('signUp.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Account does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/delete-account', methods=['POST'])
@login_required
def deleteAccount(): 
    userId = json.loads(request.data)
    posts = Product.query.filter_by(userId=userId).all()
    user = User.query.filter_by(id=userId).first()

    db.session.delete(user)
    db.session.commit()
    for i in range(len(posts)):
        db.session.delete(posts[i])
        db.session.commit()

    flash('Account deleted.', category='success')
    return render_template('login.html', user=current_user)

@auth.route('/verify/<token>', methods=['POST', 'GET'])
def verify(token):
    try:
        email = s.loads(token, max_age=300)
    except SignatureExpired:
        return render_template('verification.html', user=current_user, state='error')
    
    db.session.add(newUserGlobal)
    db.session.commit()
    login_user(newUserGlobal, remember=True)
    flash('Account created!', category='success')
    return redirect(url_for('views.home'))
