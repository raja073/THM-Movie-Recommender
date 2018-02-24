import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

from sqlalchemy import create_engine
from sqlalchemy import Column, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_string = 'postgresql://postgres:dinkan124!@localhost/movierec'

db = create_engine(db_string)
base = declarative_base()

class Movies(base):
	__tablename__ = 'movies'
	imdb_id = Column(Text, primary_key=True)
	title = Column(Text, index=True)
	rated = Column(Text, index=True)
	release_date = Column(Text, index=True)
	runtime = Column(Text, index=True)
	genre = Column(Text, index=True)
	director = Column(Text, index=True)
	writer = Column(Text, index=True)
	actor = Column(Text, index=True)
	plot = Column(Text, index=True)
	language = Column(Text, index=True)
	country = Column(Text, index=True)
	imdb_rating = Column(Text, index=True)
	production = Column(Text, index=True)
	poster = Column(Text, index=True)

Session = sessionmaker(db)
session = Session() 

def insertIntoDatabase(result, id):
	imdb = id
	title = result['Title']
	rated = result['Rated']
	release_date = result['Released']
	runtime = result['Runtime']
	genre = result['Genre']
	director = result['Director']
	writer = result['Writer']
	actor = result['Actors']
	plot = result['Plot']
	language = result['Language']
	country = result['Country']
	production = result['Production']
	imdb_rating = result['imdbRating']
	poster = result['Poster']

	movie = session.query(Movies).filter_by(imdb_id=imdb).first()
	if movie is None:
		new_movie = Movies(imdb_id=imdb, title=title, rated=rated, release_date=release_date, genre=genre,
						director=director, writer=writer, actor=actor, plot=plot, language=language, poster=poster,
						country=country, imdb_rating=imdb_rating, production=production, runtime=runtime)
		session.add(new_movie)
		session.commit()
		print("Added movie: %s, IMDB id: %s to Database!!"%(title,imdb))
	else:
		print("Movie {} already exist in Database!!".format(title))



