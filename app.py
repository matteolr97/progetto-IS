import bcrypt
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_nav import Nav



app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890abcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password  = db.Column(db.String(200), nullable=False)
    idCard = db.Column(db.String(9), unique=True, nullable=False)
    travel = db.relationship('Travel', backref='author', lazy=True)

    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')"


class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Travel('{self.destination}', '{self.date_posted}')"

@app.before_first_request
def create_all():
    db.create_all()
    db.session.commit()
@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/main')
def home2():
    return render_template('layout.html')


@app.route('/registerdb',methods=['POST','GET'])
def registerdb():
    formRed = RegistrationForm()
    if formRed.validate_on_submit():
        password_1=bcrypt.generate_password_hash(formRed.password.data)
        new_user=User(image_file=formRed.img.data,username=formRed.username.data,email=formRed.email.data,password=password_1, idCard=formRed.id.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('login')
    return render_template('register.html',formRed=formRed)



posts = [
    {
        'author' : 'Matteo La Rosa',
        'title': 'Platform post 1',
        'content' : 'First Post content',
        'date_posted' : 'November 13 2019'
    },
    {
        'author' : 'Benedetta La Rosa',
        'title' : 'Platform post 2',
        'content' : 'Second Post content',
        'date_posted' : 'November 14 2019'
    }
]

@app.route('/home')
def home():
    return render_template('home.html', posts=posts )

@app.route('/about')
def about():
    return render_template('about.html', title='About ')
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash('Account created for {form.username}!', 'success')
#         return redirect(url_for('home'))
#
#     return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    st=User.query.filter_by(email=form.email.data).first()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(st.password,form.password.data):
            flash('You have been logged in!', 'success')
        else:
            flash('Login unsussesful. Check username and password', 'danger')
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            print(image)

            return redirect(request.url)


    return render_template("public/upload_image.html")


if __name__ == '__main__':
    app.run()



