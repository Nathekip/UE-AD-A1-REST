from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
PORT_SHOWTIME = 3202
HOST = '0.0.0.0'
IP = "127.0.0.1"

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

def write_booking():
   with open('{}/databases/bookings.json'.format("."), "w") as file:
      json.dump({"bookings":bookings}, file, indent=2)

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings/<userid>", methods=["POST"])
def add_booking(userid):
   # récupérer date et film à partir du json
   req = request.get_json()
   date_mv = req['date']
   movieid = req["movieid"]
   # récupérer liste des films programmés à X date en faisant appel à l'API Showtime et vérifier si le film correspond
   response = requests.get(f"http://{IP}:{PORT_SHOWTIME}/showmovies/{date_mv}")
   # date présente dans la programmation du Cinéma ?
   if response.status_code != 200:
      return make_response({"error":"no movie at this date"}, 400)
   # film_id présent dans la liste de films ?
   if movieid not in response.json()["movies"]:
      return make_response({"error":"this movie is not programmed for this date"}, 400)
   for booking in bookings:
      if userid == booking["userid"]:
         for date in booking["dates"]:
            if str(date["date"]) == str(date_mv):
               for movie in date["movies"]:
                  if movie == movieid:
                     return make_response({"error":"an existing item already exists"}, 409)
               date["movies"].append(movieid)
               write_booking()
               return make_response(jsonify(booking),200)
         booking["dates"].append({"date": date_mv,
                                     "movies": [movieid]
                                    })
         write_booking()
         return make_response(jsonify(booking),200)
   bookings.append({"userid": userid,
                    "dates": [
                    {
                       "date": date_mv,
                       "movies": [movieid]
                    }
                    ]
                  })
   write_booking()
   return make_response(jsonify(booking), 200)

@app.route("/bookings", methods=["GET"])
def get_bookings():
   return make_response(jsonify(bookings), 200)

@app.route("/bookings/<userid>", methods=["GET"])
def get_bookings_byuser(userid):
   for booking in bookings:
      print(booking)
      if str(booking["userid"]) == str(userid):
         return make_response(jsonify(booking), 200)
   return make_response(jsonify({"error":"User ID not found"}),400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)