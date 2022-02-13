from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def to_dict(cafe):
    cafe_dict = {
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,

        # add amenities as a separate attribute
        "amenities": {
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        }
    }
    return cafe_dict


@app.route("/")
def home():
    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    cafes = Cafe.query.all()
    random_cafe = choice(cafes)

    # construct dict
    cafe = to_dict(random_cafe)
    return jsonify(cafe)


# HTTP GET - All cafes
@app.route("/all")
def all_cafes():
    cafes = Cafe.query.all()
    # make a method that creates dictionary for all cafe objects
    # loop through all cafes and create a list of dictionaries
    cafe_list = [to_dict(cafe) for cafe in cafes]
    return jsonify(cafe_list)


# HTTP GET - Fetch Cafe in a particular location
@app.route("/search")
def search_cafe():
    if request.args.get("location"):
        location = request.args.get("location")

        cafes = Cafe.query.filter_by(location=location).all()
        print(cafes)
        if cafes:
            return jsonify([to_dict(cafe) for cafe in cafes])
        else:
            return "No cafe exist at this location!"
    else:
        return "Location not found"

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
