from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Movies, Feedback
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='Home')


@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid Username or Password')
			return redirect(url_for('index'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('registration.html', title='Register', form=form)


@app.route('/movies/<int:page_num>', methods=['GET','POST'])
@app.route('/movies/<int:page_num>/<string:imdb_id>', methods=['GET','POST'])
def movies(page_num, imdb_id='0000'):
	movies = Movies.query.paginate(per_page=6, page=page_num, error_out=True)
	if request.method == 'POST':
		movie = Movies.query.filter_by(imdb_id=imdb_id).first()
		user_old = Feedback.query.filter_by(feed_id=(str(current_user.id)+'_'+movie.imdb_id)).first()
		if user_old:
			if (request.form['submit'] == 'Like' and user_old.feedback == 1) or (request.form['submit'] == 'Dislike' and user_old.feedback == -1):
				pass
			elif (request.form['submit'] == 'Like' and user_old.feedback == -1):
				user_old.feedback = 1
			elif (request.form['submit'] == 'Dislike' and user_old.feedback == 1):
				user_old.feedback = -1
			db.session.commit()
			return redirect(url_for('movies', page_num=page_num))
		else:
			if request.form['submit'] == 'Like':
				fb = Feedback(feed_id=(str(current_user.id)+'_'+movie.imdb_id), movie_id=movie.imdb_id, user_id=current_user.id, feedback=1)
			elif request.form['submit'] == 'Dislike':
		 		fb = Feedback(feed_id=(str(current_user.id)+'_'+movie.imdb_id), movie_id=movie.imdb_id, user_id=current_user.id, feedback=-1)
			db.session.add(fb)
			db.session.commit()
			return redirect(url_for('movies', page_num=page_num))
	elif request.method == 'GET':
		return render_template('movies.html', title='Movies', movies=movies)
	return render_template('movies.html', title='Movies', movies=movies)


@app.route('/coldstart', methods=['GET','POST'])
def coldstart():
	movies = Movies.query.limit(20).all()
	return render_template('coldstart.html', title='Coldstart', movies=movies)	

