from flask import Flask, render_template, request, jsonify, make_response
import os
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'databases/times.json')


with open(json_path, "r") as jsf:
   schedule = json.load(jsf)

@app.route("/", methods=['GET'])
def home():
   """
   Page d'accueil
   """
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes",methods=['GET'])
def get_json():
    """ 
    Retourne la liste des horaires
    """
    res = make_response(jsonify(schedule),200)
    return res
 
@app.route("/showmovies/<date>",methods=['GET'])
def get_schedule_bydate(date):
   """ 
   Retourne les films programmés à une date donnée
   """
   for day in schedule["schedule"] :
      if str(day["date"]) == str(date) :
         res = make_response(jsonify(day),200)
         return res
   return make_response(jsonify({"error":"date not found"}),400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)