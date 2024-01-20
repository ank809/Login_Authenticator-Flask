from flask import Flask , render_template, url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='secret_key'
db= SQLAlchemy(app)
app.app_context().push()

# db.Model is provided by Flask-SQLAlchemy and is a base class for all models.
# UserMixin is a mixin class provided by Flask-Login, which adds some common methods used for managing user authentication.
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False, unique=True)
    password= db.Column(db.String(80), nullable=False)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)