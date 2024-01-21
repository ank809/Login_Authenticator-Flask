from flask import Flask , render_template, url_for, redirect
from flask_login import UserMixin
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length

app= Flask(__name__)
bcrypt= Bcrypt(app)
app.config['MONGO_URI']='mongodb://localhost:27017/login'
app.config['SECRET_KEY']='secret_key'
mongo= PyMongo(app)
login_manager= LoginManager(app)
# When a user tries to access a protected route then it redirect the user to to specified login view(login)
login_manager.login_view= 'login' # --> end point for  login page 

class User(UserMixin):
    def __init__(self, username, password, user_id):
        self.id= user_id
        self.username = username
        self.password = password


# This function is imp because it maintains user sessions. On subsequent Flask needs to reconstruct user object based on stored user ID
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.login.find_one({"_id": user_id})
    if user_data:
        return User(username=user_data['username'], password=user_data['password'])
    return None


class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password= PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password" })
    submit= SubmitField("Register")

    def validate_username(self, username):
        existing_user_username=mongo.db.login.find_one({"username":username.data})
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one')
        
class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password= PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password" })
    submit= SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods= ['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        userdata= mongo.db.login.find_one({"username":form.username.data})
        if userdata and bcrypt.check_password_hash(userdata['password'], form.password.data):
            user= User(username= userdata['username'], password= userdata['password'], user_id= userdata['_id'])
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form= RegisterForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user={"username": form.username.data, "password": hashed_password}
        mongo.db.login.insert_one(new_user)
        return redirect(url_for('login'))
    return render_template('register.html', form= form)

if __name__== '__main__':
    app.run(debug=True)