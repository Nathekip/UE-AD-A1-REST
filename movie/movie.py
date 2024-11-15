from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'databases/movies.json')

with open(json_path, "r") as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

@app.route("/help", methods=['GET'])
def get_help():
    endpoints = ["/json","/movies/{movieid}","/movies/{movieid}/{rate}","/addmovie/{movieid}","/movies/{movieid}","/moviesbytitle"]
    html = f"<h1>Endpoints : </h1><ul>{''.join([f'<li>{path}</li>' for path in endpoints])}</ul>"
    return make_response(html, 200)

@app.route("/json",methods=['GET'])
def get_json():
    res = make_response(jsonify(movies),200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    if request.args:
        req = request.args
        title = req["title"][1:-1]
    for movie in movies:
        if movie["title"] == title:
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie not found"}),400)

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie),200)
            return res
    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

def write(movies):
    with open(json_path, "w") as jsf:
        json.dump({"movies":movies}, jsf)

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)