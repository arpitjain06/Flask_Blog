from datetime import datetime
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
print(app, "=============")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'c7905cb73417512f922266ffa4f8ab8f'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique =True, nullable=False)
	email = db.Column(db.String(120), unique =True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__():
		return f"Post('{self.title}', '{self.date_posted}')"

posts= [
	{
		'autho':"arpit jain",
		"title": "blog post1",
		"content":"First post content",
		"date_posted": "April 28, 2018"
	},
	{
		'autho':"anshul jain",
		"title": "blog post1",
		"content":"First post content",
		"date_posted": "April 28, 2019"
	}
]

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html", posts=posts)
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'

@app.route('/about')
def about():
	return render_template("about.html", title="about")
	# name = request.args.get("k", "Page")
	# return f'about, {escape(name)}!'

@app.route('/contact_us')
def contact_us():
	name = request.args.get("us", "")
	return f'Contact, {escape(name)}!'


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', '_success_')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login')	
def login():
	form = LoginForm()
	return render_template('login.html', title='login', form=form)

if __name__ == '__main__':
	app.run(debug=True)
 