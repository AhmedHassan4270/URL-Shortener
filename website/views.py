#Create our first website route

from flask import Blueprint,render_template,request, flash,redirect
from flask_login import login_required, current_user
from .models import Favourite_URL,Urls
from . import db
import string
import random

#Blueprint object allow static files, templates, and views that are associated with routes in app.
views=Blueprint('views',__name__) # This file is a blueprint of our app.
                                  

# This route has define how to save favourite URL in notes.
@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST': 
        favourite_url = request.form.get('favourite_url')#Gets the note from the HTML 

        if len(favourite_url) < 8:
            flash('Data is too short! It Must Be Greater Than 8 Characters.', category='error') 
        else:
            new_favourite_url = Favourite_URL(data=favourite_url, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_favourite_url) #adding the note to the database 
            db.session.commit()
            flash('Favourite_URL Added!', category='success')
    return render_template("home.html", user=current_user)

# This route has define how to delete unlike favourite URL in notes.
@views.route("/delete/<int:id>")
def delete(id):
    deleteFavourite_URL = Favourite_URL.query.filter_by(id=id).first()
    db.session.delete(deleteFavourite_URL)
    db.session.commit()
    flash('Favourite_URL Delete! ', category='success')
    return redirect("/")

# This route has define take long URL then convert into short URL.
@views.route('/shortner', methods=['POST', 'GET'])
def required_shortner():
    if request.method == "POST":
        url_received = request.form["nm"]
        # check if url already exits in DB
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            short=found_url.short
            return render_template('shorturl.html', long_url_display=url_received,short_url_display=short,user=current_user)
        else:
            short_url = shorten_url()
            new_short =Urls(short=short_url,long=url_received, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_short)
            db.session.commit()
            flash('Short URL generated!', category='success')
            return render_template('shorturl.html', long_url_display=url_received,short_url_display=short_url,user=current_user)

    else:
        return render_template('home.html',user=current_user)

# This function generate shorter URL code with the combination of lower and uper case.
def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=6) # for example =["a","F","L","e","S","p"]
        rand_letters = "".join(rand_letters)    # list convert into string.
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters
    
# This route has allow to user.If short URL save in DB & Short URL get request then visit to long URL page.
@views.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return '''
    <body style="background-color: #DCDCDC;">
        <h2 style="color: Black ;">This Shortener URL Does Not Exist In DataBase</h2>
        <h3 style="color: Red ;">Note : You Can Use Only Those Shortener URL That Are Save In DataBase</h3>
        <input type="button" value="Back to Home" class="btn btn-primary" onclick="history.back()"/>
    </body>
    '''
# This route has allowto user to checked how many URL save in personal DB.
@views.route('/all_urls',methods=['GET','POST'])
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all(),user=current_user)
