# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import json
import logging
## scraping parameters
explorer_label = {"scope":"row","style":"white-space:nowrap;padding-right:0.65em;"}
year_label = {"style":"padding:0.1em 0;line-height:1.2em;white-space:normal;"}
movie_label = {"class":"mw-headline", "id":"Film"}

## urls
url_prefix = "https://en.wikipedia.org"
example_movie = "/wiki/Titanic_(1997_film)"
example_actor = "/wiki/Ben_Whishaw"

def scrape_movie_page(url):
	'''
	scrape a movie page
	:param url: the url of the page
	:return: movie_info: movie information dictionary
			actor_dir: the urls of actor pages to be crawled
	'''
	source_html = BeautifulSoup(urlopen(url), "lxml")

	star_list = source_html.find("th", explorer_label, text = "Starring")\
			.find_next_sibling("td").find_all("a")
	box_office = source_html.find("th", explorer_label, text = "Box office")\
	        .find_next_sibling("td").get_text()
	year = source_html.find("div", year_label, text = "Release date")\
			.find_parent().find_next_sibling("td").find_all("li")[0].get_text()
	year = re.findall(r"19\d\d|20\d\d", year)[0]

	actor_dir = {}
	for star in star_list:
	    actor_dir[star.get_text()] = star['href']
	movie_info = {"actors":list(actor_dir.keys()),\
				 "grossing":amount2num(box_office), \
				 "year":year}
	return movie_info, actor_dir

def scrape_actor_page(url):
	'''
	scrape an actor page
	:param url: the url of the page
	:return: actor_info: actor information dictionary
			movie_dir: the urls of movie pages to be crawled
	'''
	source_html = BeautifulSoup(urlopen(url), "lxml")

	age = source_html.find("th", scope="row", text="Born")\
			.find_next_sibling("td").find(text=re.compile('age'))
	age = re.findall(r"\d\d", age)[0]
	movie_list = source_html.find("span", movie_label, text = "Film")\
			.find_parent().find_next_sibling("table").find_all("i")

	movie_dir = {}
	for movie in movie_list:
		try:
			movie = movie.find("a")
			movie_dir[movie.get_text()] = movie['href']
		except(TypeError):
			continue
	actor_info = {"movies":list(movie_dir.keys()),\
				 "age":age}
	return actor_info, movie_dir

def amount2num(amount):
	'''
	change grossing value to number
	:param amount: grossing value
	:return: numeric value
	'''
	num = re.findall(r"\d*\.\d+|\d+", amount)[0]
	num = float(num)
	amount = amount.lower()
	if "billion" in amount:
	    num *= 1e9
	elif "million" in amount:
	    num *= 1e6
	elif "thousand" in amount:
	    num *= 1e3
	return num

def crawl(source, name, is_movie = True):
	'''Running the crawler
	source: source page url
	name: the name of the source wiki
	is_movie: true if the source page is the wiki of a movie
			false if is of an actor
	'''
	#intial_setting
	start_time = time.time()
	logging.basicConfig(filename='crawler.log',level=logging.INFO)
	#crawling gloabal setting
	actor_count = 0
	movie_count = 0
	movie_crawled = {}
	actor_crawled = {}
	movie_to_crawl = {}
	actor_to_crawl = {}
	if is_movie:
		movie_to_crawl[name] = source
	else:
		actor_to_crawl[name] = source
	#running the crawler
	while(len(movie_crawled) < 125 or len(actor_crawled) < 250):
		if is_movie:
			movie_count += crawl_pages(movie_crawled, movie_to_crawl, actor_to_crawl, 5, scrape_movie_page)
			print("Movies crawled: %d" % movie_count)
		else:
			actor_count += crawl_pages(actor_crawled, actor_to_crawl, movie_to_crawl, 10, scrape_actor_page)
			print("Actors crawled: %d" % actor_count)
		is_movie = not is_movie
	#dump crawled information
	dump_crawled_info(actor_crawled, movie_crawled)
	print("--- %s seconds ---" % (time.time() - start_time))


def dump_crawled_info(actor_crawled, movie_crawled):
	'''dump crawled information of files'''
	actors = open("actors_info.json", "w")
	movies = open("movies_info.json", "w")
	json.dump(actor_crawled, actors)
	json.dump(movie_crawled, movies)
	actors.close()
	movies.close()

def crawl_pages(name_crawled, name_to_crawl, other_to_crawl, count, scrape_funtion):
	'''
	crawl the movie/actor pages
	:param name_crawled: names have been crawled
	:param name_to_crawl: names to be crawled
	:param other_to_crawl: the other type of names to be crawl
	:param count: the maximum number of pages to crawl in a row
	:param scrape_funtion: the function to scrape the page
	:return: the number of pages crawled
	'''
	num_crawled = 0
	prompt = "movie" if scrape_funtion == scrape_movie_page else "actor"
	while (name_to_crawl != {}):
		name, url = name_to_crawl.popitem()
		if name not in name_crawled:
			logging.info('Start scraping %s :%s' % (prompt,name))
			try:
				name_info, other_dir = scrape_funtion(url_prefix + url)
			except:
				logging.warning('Quit scraping %s :%s' %  (prompt,name))
			else:
				logging.info('Finished scraping %s :%s' %  (prompt,name))
				name_crawled[name] = name_info
				other_to_crawl.update(other_dir)
				count -= 1
				num_crawled += 1
				if count <= 0:
					break
			time.sleep(0.1)
	return num_crawled


crawl(example_movie, "Titanic")
#crawl(example_actor, "Ben Whishaw"， is_movie = False)


