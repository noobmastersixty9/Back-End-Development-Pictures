from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({"message": "Picture not found"}), 404




######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.json:
        abort(400, description="Not a JSON request")

    new_picture = request.json

    # Check if 'id' is in the new_picture data and if it's a duplicate
    if 'id' in new_picture and any(picture['id'] == new_picture['id'] for picture in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # Assuming there's a mechanism to assign an ID if not provided, or it's okay to append without an ID
    data.append(new_picture)  # Adding the new picture to the data list.
    return jsonify(new_picture), 201

    
######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item.get("id") == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404
    
    if not request.json:
        abort(400, description="Not a JSON request")
    
    # Update picture's info from request.json, except the 'id' field.
    for key, value in request.json.items():
        if key != "id":
            picture[key] = value
    
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data  # Reference the global 'data' variable to modify it.
    index_to_delete = next((index for index, item in enumerate(data) if item.get("id") == id), None)
    if index_to_delete is not None:
        del data[index_to_delete]
        return {"message": "picture deleted successfully"}, 204
    else:
        return {"message": "picture not found"}, 404
