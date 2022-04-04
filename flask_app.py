
##theses are the imports that are made
from flask import Flask,render_template,redirect,url_for,session,request,abort
##Importing the Form from the other python file
from forms import RegisterForm
##importing SQL for linking
from flask_sqlalchemy import SQLAlchemy
import os
import pathlib
##Importing google oAuth for Authorization
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests

import google.oauth2.credentials




##This is the Google Credentials which you have to change according to your credentials
GOOGLE_CLIENT_ID = "1063710188263-m4ua049kf6aef99m722ei59jgf7m1ono.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")##Path to the file where you have stored the secret credentials

##Creating a Flow mentioning the scopes and redirect uri
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],##Scopes used
    redirect_uri="https://pratham7.pythonanywhere.com/oauth2callback"##the redirect uri that you mentioned in the Google api
)

authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')


app = Flask(__name__)
app.config["DEBUG"] = True
##Details of the Database that you creatd
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="pratham7",##change to your dets
    password="Admin@1234",
    hostname="pratham7.mysql.pythonanywhere-services.com",
    databasename="pratham7$login",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

##Creating a table in the SQL using Python
db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = "Login"
    id=db.Column(db.Integer(),primary_key=True)
    username =db.Column(db.String(length=30),unique=True,nullable=False)
    email_address=db.Column(db.String(length=50),unique=True,nullable=False)
    password=db.Column(db.String(length=30),nullable=False)

##This is the essential Secret Key that you have yo add to your program otherwise it won't run
app.config['SECRET_KEY']='702d3777b1fe202adba826ec'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

##Creating the home page
@app.route("/")
@app.route("/home")
def home_page():
    #return "<p>Heading</p>"
    return render_template('home.html')##Calling the home html page created

##Displayong products using python dictonaries
##Sending data to HTML usign Python and displaying in the HTML PAGE
@app.route("/market")
def market_page():
    items = [
    {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
]
    return render_template('market.html',items=items)
##Creating a new user and saving the information to the Database Created
@app.route('/register', methods=['GET','POST'])
def register_page():
    form= RegisterForm()
    if form.validate_on_submit():
        user_to_create =User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    return render_template('register.html', form=form)




##Defining a function to check if you are logged in before using the logout function
def login_is_required(function):
    def wrapper(*args,**kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper
##Creating a page for login
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

##CHecking the redirects and states
@app.route("/oauth2callback")
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")

##Logout page
@app.route("/logout")

def logout():

    session.clear()
    del session['credentials']
    return "Log out successful"



