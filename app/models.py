from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, index=True, unique=True)
	email = db.Column(db.Text, index=True, unique=True)
	password_hash = db.Column(db.Text)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Movies(db.Model):
	imdb_id = db.Column(db.Text, primary_key=True)
	title = db.Column(db.Text, index=True)
	rated = db.Column(db.Text, index=True)
	release_date = db.Column(db.Text, index=True)
	runtime = db.Column(db.Text, index=True)
	genre = db.Column(db.Text, index=True)
	director =db.Column(db.Text, index=True)
	writer = db.Column(db.Text, index=True)
	actor = db.Column(db.Text, index=True)
	plot = db.Column(db.Text, index=True)
	language = db.Column(db.Text, index=True)
	country = db.Column(db.Text, index=True)
	imdb_rating = db.Column(db.Text, index=True)
	production = db.Column(db.Text, index=True)
	poster = db.Column(db.Text, index=True)

	def __repr__(self):
		return '<Movie {}>'.format(self.title)

class Feedback(db.Model):
	feed_id = db.Column(db.Text, primary_key=True)
	user_id = db.Column(db.Integer)
	movie_id = db.Column(db.Text)
	feedback = db.Column(db.Integer)

	def __repr__(self):
		return '<Feedback {}>'.format(self.fb_id)