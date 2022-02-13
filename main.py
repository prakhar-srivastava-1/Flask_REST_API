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


# Helper Methods
def to_dict(cafe):
    cafe_dict = {
        "id": cafe.id,
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


def check_bool(has_attribute):
    if has_attribute in ["true", "True", "1"]:
        return True
    return False


# Routes
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
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe()
    new_cafe.name = request.form.get("name")
    new_cafe.map_url = request.form.get("map_url")
    new_cafe.img_url = request.form.get("img_url")
    new_cafe.location = request.form.get("location")
    new_cafe.seats = request.form.get("seats")
    new_cafe.has_toilet = check_bool(request.form.get("has_toilet"))
    new_cafe.has_wifi = check_bool(request.form.get("has_wifi"))
    new_cafe.has_sockets = check_bool(request.form.get("has_sockets"))
    new_cafe.can_take_calls = check_bool(request.form.get("can_take_calls"))
    new_cafe.coffee_price = request.form.get("coffee_price")
    try:
        db.session.add(new_cafe)
        db.session.commit()
    except:
        return jsonify(
            {
                "response": {
                    "failure": "Cafe could not be added!"
                }
            }
        )
    return jsonify(
        {
            "response": {
                "success": "Successfuly added the new cafe!"
            }
        }
    )


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # grab the cafe object
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    try:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
    except:
        return jsonify({"response": {"failure": "Update failed!"}})
    return jsonify({"response": {"success": f"Coffee Price updated successfully for Cafe {cafe_id}!"}})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    if request.args.get("api-key") != "TopSecretAPIKey":
        return jsonify(error={"error": "Sorry you can't perform this action!"}), 403
    try:
        cafe = Cafe.query.filter_by(id=cafe_id).first()
        db.session.delete(cafe)
        db.session.commit()
    except:
        return jsonify(error={"error": "Sorry a cafe with this ID doesn't exist!"}), 404
    return jsonify(success={"success": f"Cafe with ID {cafe_id} deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
