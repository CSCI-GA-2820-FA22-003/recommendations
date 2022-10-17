"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Recommendation

# Import Flask application
from . import app

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendations REST API Service",
            version="1.0",
            #paths=url_for("list_recommendations", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Recommendation.init_db(app)

######################################################################
# CREATE A RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendation():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    #check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    #location_url = url_for("get_pets", pet_id=pet.id, _external=True)

    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED


######################################################################
# LIST ALL Recommendations
######################################################################
@app.route("/recommendations/list", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendations list")
    pets = []
    category = request.args.get("recommendation_type")
    if category:
        recommendations = Recommendation.find_by_category(category)
    else:
        recommendations = Recommendation.all()

    results = [recommendation.serialize() for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK