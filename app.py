#!flask/bin/python
from flask import Flask, jsonify, request, make_response, abort
import json
import re

with open("data.json") as f:
    data = json.load(f)

actors = data[0]
movies = data[1]
NAME = "name"
AGE = "age"
YEAR = "year"
TOTAL_GROSS = 'total_gross'
BOX_OFFICE = 'box_office'

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/network/api/actors/<string:name>', methods=['GET'])
def get_actor(name):
    '''
    get an actor by name
    :param name: the name of the actor
    :return: the information dictionart of the actor
    '''
    name = name.replace('_', ' ')
    if name in actors:
        return jsonify(actors[name])
    else:
        abort(404)

@app.route('/network/api/actors', methods=['GET'])
def filter_actors():
    '''
    filter actors by query
    query using capitalized python keyword AND OR NOT IN
    :return: a dictionary of filtered actors
    '''
    query = request.query_string.decode("utf-8")
    filtered = {}
    query = query.replace('AND', ' and ').replace('OR', ' or ').replace('NOT', ' not ')\
            .replace('age=', 'actors[actor][AGE]==').replace('INname', ' in actors[actor][NAME]')
    for actor in actors:
        if eval(query):
            filtered[actor] = actors[actor]
    if len(filtered) == 0:
        abort(404)
    return jsonify(filtered)

@app.route('/network/api/movies/<string:name>', methods=['GET'])
def get_movie(name):
    '''
    get a movie by name
    :param name: the name of the movie
    :return: the information of the movie
    '''
    name = name.replace('_', ' ')
    if name in movies:
        return jsonify(movies[name])
    else:
        abort(404)


@app.route('/network/api/movies', methods=['GET'])
def filter_movies():
    '''
    filter movies by query
    query using capitalized python keyword AND OR NOT IN
    :return: a dictionary of filtered movies
    '''
    query = request.query_string.decode("utf-8")
    filtered = {}
    query = query.replace('AND', ' and ').replace('OR', ' or ').replace('NOT', ' not ')\
            .replace('year=', 'movies[movie][YEAR]==').replace('INname', ' in movies[movie][NAME]')
    for movie in movies:
        if eval(query):
            filtered[movie] = movies[movie]
    if len(filtered) == 0:
        abort(404)
    return jsonify(filtered)

@app.route('/network/api/actors/<string:name>', methods=['PUT'])
def update_actor(name):
    '''
    update the information of an existing actor
    :param name: the name of the actor
    :return: the dictionary of updated information
    '''
    name = name.replace('_', ' ')
    update_dir = request.json
    if name in actors:
        if AGE in update_dir:
            actors[name][AGE] = update_dir[AGE]
        elif TOTAL_GROSS in update_dir:
            actors[name][TOTAL_GROSS]=update_dir[TOTAL_GROSS]
        else:
            abort(400)
    else:
        abort(400)
    return jsonify(update_dir)


@app.route('/network/api/movies/<string:name>', methods=['PUT'])
def update_movie(name):
    '''
    update the information of an existing movie
    :param name: the name of the movie
    :return: the dictionary of updated information
    '''
    name = name.replace('_', ' ')
    update_dir = request.json
    if name in movies:
        if YEAR in update_dir:
            movies[name][YEAR] = update_dir[YEAR]
        elif BOX_OFFICE in update_dir:
            movies[name][BOX_OFFICE]=update_dir[BOX_OFFICE]
        else:
            abort(400)
    else:
        abort(400)
    return jsonify(update_dir)

@app.route('/network/api/actors', methods=['POST'])
def add_actor():
    '''
    add an actor to the actors list
    :return: 201 if added, 400 if failed
    '''
    update_dir = request.json
    try:
        name = update_dir[NAME]
    except:
        abort(400)
    else:
        if name not in actors:
            actors[name] = update_dir
        else:
            abort(400)
    return jsonify({name:update_dir}), 201


@app.route('/network/api/movies', methods=['POST'])
def add_movie():
    '''
    add a movie to the movies list
    :return: 201 if added, 400 if failed
    '''
    update_dir = request.json
    try:
        name = update_dir[NAME]
    except:
        abort(400)
    else:
        if name not in movies:
            movies[name] = update_dir
        else:
            abort(400)
    return jsonify({name:update_dir}), 201

@app.route('/network/api/actors/<string:name>', methods=['DELETE'])
def del_actor(name):
    '''
    delete an actor from the actors list
    :param name: the name of the actor
    :return: 200 if deleted, 400 if failed
    '''
    name = name.replace('_', ' ')
    if name in actors:
        del actors[name]
    else:
        abort(400)
    return jsonify({}), 200

@app.route('/network/api/movies/<string:name>', methods=['DELETE'])
def del_movie(name):
    '''
    delete a movie from the movies list
    :param name: the name of the movie
    :return: 200 if deleted, 400 if failed
    '''
    name = name.replace('_', ' ')
    if name in movies:
        del movies[name]
    else:
        abort(400)
    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True)
