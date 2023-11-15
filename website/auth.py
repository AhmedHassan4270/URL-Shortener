from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # Werkzueg (a key component of Flask) provides a library for hashing passwords.
from . import db   #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


#Blueprint object allow static files, templates, and views that are associated with routes in app.
auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Please Try Again.', category='error')
        else:
            flash('Email Does Not Exist.', category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # First checked user email in Database.
        if user:
            flash('Email Already Exists.', category='error')
        elif len(email) < 11:
            flash('Email Must Be Greater Than 10 Characters.', category='error')
        elif len(first_name) < 4:
            flash('First Name Must Be Greater Than 3 Character.', category='error')
        elif len(last_name) < 4:
            flash('Last Name Must Be Greater Than 3 Characte.', category='error')
        elif password1 != password2:
            flash('Passwords Don\'t Match.', category='error')
        elif len(password1) < 7:
            flash('Password Must Be At Least 7 characters.', category='error')
        else:      
            new_user = User(email=email, first_name=first_name, last_name=last_name,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)  # New user data add in table of Database.
            db.session.commit()       # New user data save in table of Database.
            flash('Account Created!', category='success')
            login_user(new_user, remember=True) # New user allow to access home page of view.py
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)