from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import os
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
PORT_BOOKING = 3201
PORT_MOVIE = 3200
HOST = '0.0.0.0'
IP = '127.0.0.1'

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'databases/users.json')

with open(json_path, "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   """
   Page d'accueil
   """
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users",methods=['GET'])
def get_json():
    """
    Retourne la liste des utilisateurs
    """
    res = make_response(jsonify(users),200)
    return res
 
@app.route("/users", methods=['POST'])
def add_user():
    """ 
    Ajouter un utilisateur
    """
    new_user = request.get_json()
    users.append(new_user)
    with open(json_path, "w") as jsf:
        json.dump({"users": users}, jsf, indent=2)
    return make_response(jsonify(new_user), 201)
 
@app.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ 
    Supprimer un utilisateur
    """
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            with open(json_path, "w") as jsf:
                json.dump({"users": users}, jsf, indent=2)
            return make_response(jsonify({"message": "user deleted"}), 200)
    return make_response(jsonify({"error": "user not found"}), 404)
 
@app.route("/users/<user_id>/bookings", methods=['POST'])
def add_booking_for_user(user_id):
    """
    Ajouter une réservation pour un utilisateur
    """
    booking_data = request.get_json()
    response = requests.post(f"http://{IP}:{PORT_BOOKING}/bookings/{user_id}", json=booking_data)
    if response.status_code != 200:
        return make_response({"error": "could not add booking"}, 400)
    return make_response(response.json(), 200)

@app.route("/users/bookings/<user>",methods=['GET'])
def get_bookings_byuser(user):
   """ 
   Retourne les réservations d'un utilisateur
   """
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
   """
   Retourne les films réservés par un utilisateur
   """
   id = -1
   # Trouver l'utilisateur par nom ou ID
   for useri in users :
      if useri["name"] == user or useri["id"] == user :
         id = useri["id"]
         break
   if id == -1 :
      return make_response(jsonify({"error":"user not found"}),400)
   
   # Récupérer les réservations de l'utilisateur
   response = requests.get(f"http://{IP}:{PORT_BOOKING}/bookings/{id}")
   if response.status_code != 200:
      return make_response({"error":"no bookings for this user"}, 400)
   movies_json = {"movies" : []}
   
   # Parcourir les dates de réservation et récupérer les détails des films
   for movies in response.json()["dates"] :
      for movie in movies["movies"] :
         movie_json = requests.get(f"http://{IP}:{PORT_MOVIE}/movies/{movie}")
         print(response.json())
         movies_json["movies"].append(movie_json.json())
         
   print(movies_json)
   return make_response(jsonify(movies_json),200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
