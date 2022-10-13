import email
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
# Add Database
# Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kentsu1976@localhost/our_users'
# SECRET KEY
app.config['SECRET_KEY'] = "My super secret key that no one is supposed to know"
#Initialize The Database
db = SQLAlchemy(app)






# Create Model (what to save to the database)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) # Cannot be empty field = nullable
    email = db.Column(db.String(120), nullable=False, unique=True) # Must be unique address = unique
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated Successfully!")
            return render_template("update.html",
                form = form,
                name_to_update = name_to_update)
        except:
            flash("Oh, No! Looks, like there were a problem... try again!")
            return render_template("update.html",
                form = form,
                name_to_update = name_to_update)
    else:
        return render_template("update.html",
                    form = form,
                    name_to_update = name_to_update) 

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")




#def index():
#    return "<h1>Hello World!</h1>"

# FILTERS!!!
#safe (poistaa html-koodin)
#capitalize (muuttaa jokaisen sanan ensimmäisen kirjaimen isoksi)
#lower  (muuttaa tekstin pieneksi)
#upper  (muuttaa tekstin isoksi)
#title  
#trim
#trim (poistaa välit)
#striptags

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users) 

# Create a route decorator
@app.route('/')

def index():
    first_name = "Tero"
    stuff = "This is <strong>Bold</strong> Text"
    
    favorite_pizza = ["pepperoni", "Onion", "Cheese", "Bell Pepper", 41]
    return render_template('index.html', first_name=first_name, stuff=stuff,
    favorite_pizza=favorite_pizza)

# localhost:5000/user/Tero
@app.route('/user/<name>')

def user(name):
    return render_template('user.html', name=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)

def page_not_found(e):
    return render_template('500.html'), 500

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
        
    return render_template('name.html',
        name = name,
        form = form)
