from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
PORT_BOOKING = 3201
PORT_MOVIE = 3200
HOST = '0.0.0.0'
IP = '127.0.0.1'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users",methods=['GET'])
def get_json():
    res = make_response(jsonify(users),200)
    return res

@app.route("/users/bookings/<user>",methods=['GET'])
def get_bookings_byuser(user):
   id = -1
   for useri in users :
      if useri["name"] == user or useri["id"] == user :
         id = useri["id"]
         break
   if id == -1 :
      return make_response(jsonify({"error":"user not found"}),400)
   response = requests.get(f"http://{IP}:{PORT_BOOKING}/bookings/{id}")
   if response.status_code != 200:
      return make_response({"error":"no bookings for this user"}, 400)
   return make_response(response.json())

@app.route("/users/movies/<user>",methods=['GET'])
def get_movies_byuser(user):
   id = -1
   for useri in users :
      if useri["name"] == user or useri["id"] == user :
         id = useri["id"]
         break
   if id == -1 :
      return make_response(jsonify({"error":"user not found"}),400)
   response = requests.get(f"http://{IP}:{PORT_BOOKING}/bookings/{id}")
   if response.status_code != 200:
      return make_response({"error":"no bookings for this user"}, 400)
   movies_json = {"movies" : []}
   for movies in response.json()["dates"] :
      for movie in movies["movies"] :
         movie_json = requests.get(f"http://{IP}:{PORT_MOVIE}/movies/{movie}")
         print(response.json())
         movies_json["movies"].append(movie_json.json())
   print("test")
   print(movies_json)
   return make_response(jsonify(movies_json),200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
