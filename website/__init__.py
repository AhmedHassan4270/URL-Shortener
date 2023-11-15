from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db=SQLAlchemy()


# for creating the app
def create_app():
    # initializing the app
    app = Flask(__name__) 
    # initializing the data base
    app.config['SECRET_KEY'] = 'muhammadahmedhassan111111'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    
    from .views import views
    from .auth import auth
# Now for registering the blueprints.telling the flask we have blueprints that containing views and auth file
# in which have routes to define some diffents URLs for used they are in our app.   
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
 

    from .models import User, Favourite_URL,Urls # Define Tables in Database from model.py
 
    with app.app_context():  # Create database within app context
        db.create_all()
    
    # LoginManager is needed for our application to be able to manage login 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'    #implement login required.If not login then redirect templete to name of our function 
    login_manager.init_app(app)                 

    #This is telling Flask how we load a user. Creates a user loader callback that returns the user object given an id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
        
        
        
        
        
        
        
        
        
        
# load_user is a callback function used by the flask-login login manager. When flask needs to look up and load the user related to a specific session ID, it will call this function