import json
import httplib2
from dbconnect import insertIntoDatabase

import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

tmdb_api_key = 'ed8723f4d3ff22d4cf366186e26a5291'
omdb_api_key = 'bc71e7ec'

def omdbDataFinder(imdb_id_list):
	for id in imdb_id_list:
		url = ('http://www.omdbapi.com/?i=%s&plot=short&r=json&apikey=%s'%(id,omdb_api_key))
		h = httplib2.Http()
		result = json.loads(h.request(url,'GET')[1])
		print("Found data of movie %s, from OMDB db"%(id))
		insertIntoDatabase(result, id)


def imdbIdFinder(tmdb_id_list):
	imdb_id_list = []
	for id in tmdb_id_list:
		url = ('https://api.themoviedb.org/3/movie/%s?api_key=%s&language=en-US'%(id,tmdb_api_key))
		h = httplib2.Http()
		result = json.loads(h.request(url,'GET')[1])
		imdb_id_list.append(result['imdb_id'])
	print("Found imdb ID's from TMDB db. IMDB ID's:%s"%(imdb_id_list))
	omdbDataFinder(imdb_id_list)

def popularMoviesFinder(page):
	tmdb_id_list = []
	url = ('https://api.themoviedb.org/3/movie/popular?api_key=%s&page=%s'%(tmdb_api_key,page))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	res = result['results']
	for movie in res:
		tmdb_id_list.append(movie['id'])
	print("Found polular movies page:%s, from TMDB db. Movie ID's:%s"%(page,tmdb_id_list))
	imdbIdFinder(tmdb_id_list)


if __name__ == '__main__':
 	popularMoviesFinder(5)