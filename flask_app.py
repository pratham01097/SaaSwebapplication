
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template,url_for,redirect
from forms import RegisterForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="padwani01",
    password="Admin@123",
    hostname="padwani01.mysql.pythonanywhere-services.com",
    databasename="padwani01$login",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "Login"
    id=db.Column(db.Integer(),primary_key=True)
    username =db.Column(db.String(length=30),unique=True,nullable=False)
    email_address=db.Column(db.String(length=50),unique=True,nullable=False)
    password=db.Column(db.String(length=30),nullable=False)

app.config['SECRET_KEY']='7fe5d20a83246be290178af9'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = [
    {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html',items=items)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form= RegisterForm()
    if form.validate_on_submit():
            user_to_create=User(username=form.username.data,
                                email_address=form.email_address.data,
                                password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
    return render_template('register.html', form=form)