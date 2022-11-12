"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, abort, url_for
from .common import status  # HTTP Status Codes
from service.models import Recommendation

# Import Flask application
from . import app

BASE_URL = "/recommendations"

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
            # paths=url_for("list_recommendations", _external=True),
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


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


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
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    isDuplicate = Recommendation.check_if_duplicate(recommendation.product_1, recommendation.product_2)
    if isDuplicate:
        app.logger.info("Recommendation with products [%s] and [%s] already exists.", 
                                    recommendation.product_1, recommendation.product_2)
        abort(status.HTTP_406_NOT_ACCEPTABLE, f"Recommendation with products"+ 
                        "'{recommendation.product_1}' and '{recommendation.product_1}'  already exists.")
    recommendation.create()
    message = recommendation.serialize()
    location_url = url_for("list_recommendations", recommendation_id=recommendation.id, _external=True)
    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED,{"Location":location_url}


######################################################################
# READ A Recommendation
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["GET"])
def list_recommendation(recommendation_id):
    """Returns a Recommendation requested by it's ID"""
    app.logger.info("Request for a recommendation id=%s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    result = recommendation.serialize()
    app.logger.info("Recommendation with ID [%s] has been read", recommendation.id)
    return jsonify(result), status.HTTP_200_OK


######################################################################
# LIST ALL Recommendations
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendations list")
    recommendations = []
    category = request.args.get("recommendation_type")
    product = request.args.get("product")
    if category:
        recommendations = Recommendation.find_by_category(category)
    elif product:
        recommendations = Recommendation.find_by_product(product)
    else:
        recommendations = Recommendation.all()

    results = [recommendation.serialize() for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["PUT"])
def update_recommendations(recommendation_id):
    """
    Update a Recommendation

    This endpoint will update a Recommendation based the body that is posted
    """
    app.logger.info("Request to update recommendation with id: %s", recommendation_id)

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with id '{recommendation_id}' was not found.")

    recommendation.deserialize(request.get_json())
    recommendation.id = recommendation_id
    recommendation.update()

    app.logger.info("Recommendation with ID [%s] updated.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["DELETE"])
def delete_recommendations(recommendation_id):
    """
    Delete a recommendation
    This endpoint will delete a Recommendation based the id specified in the path
    """
    app.logger.info("Request to delete Recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.delete()

    app.logger.info("Recommendation_id with ID [%s] delete complete.", recommendation_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIKE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>/like", methods=["PUT"])
def like_recommendations(recommendation_id):
    """
    Like a Recommendation

    This endpoint will liked a Recommendation given the recommendation ID
    """
    app.logger.info("Request to like recommendation with id: %s", recommendation_id)

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with id '{recommendation_id}' was not found.")

    recommendation.liked = True
    recommendation.update()

    app.logger.info("Recommendation with ID [%s] liked.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# DISLIKE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>/like", methods=["DELETE"])
def dislike_recommendations(recommendation_id):
    """
    Dislike a Recommendation

    This endpoint will dislike a Recommendation given the recommendation ID
    """
    app.logger.info("Request to dislike recommendation with id: %s", recommendation_id)

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with id '{recommendation_id}' was not found.")

    recommendation.liked = False
    recommendation.update()

    app.logger.info("Recommendation with ID [%s] disliked.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK
