"""
My Service

Describe what your service does here
"""

from flask import jsonify, request
from flask_restx import Resource, fields, reqparse, inputs
from service.models import Recommendation

# Import Flask application
from . import app, api
from .common import status  # HTTP Status Codes

BASE_URL = "/api/recommendations"

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
    """Base URL for our service"""
    app.logger.info("Base URL")
    return app.send_static_file("index.html")

######################################################################
# Configure the Root route before OpenAPI
######################################################################


# Define the model so that the docs reflect what can be sent
create_model = api.model('Recommendation', {
    'id': fields.Integer(required=True, description='The ID of the Recommendation'),
    'product_1': fields.String(required=True, description='The name of Product 1'),
    'product_2': fields.String(required=True, description='The name of Product 2'),
    'liked': fields.Boolean(required=False,
                            description='Does the customer dislike the recommendation?'),
    'recommendation_type': fields.String(required=True,
                                         description='The type of the Recommendation'),
})

recommendation_model = api.inherit(
    'RecommendationModel',
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
recommendation_args = reqparse.RequestParser()
recommendation_args.add_argument('product_1', type=str, location='args', required=False,
                                 help='List Recs by product 1')
recommendation_args.add_argument('product_2', type=str, location='args', required=False,
                                 help='List Recs by product 2')
recommendation_args.add_argument('recommendation_type', type=str, location='args', required=False,
                                 help='List Recs by category')
recommendation_args.add_argument('liked', type=inputs.boolean, location='args', required=False,
                                 help='List Recs by liked')

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


def init_db():
    """ Initializes the SQLAlchemy app """
    # global app
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

    app.logger.error("Invalid Content-Type: %s",
                     request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
#  PATH: /recommendations
######################################################################
@api.route('/recommendations', strict_slashes=False)
class PetCollection(Resource):
    """ Handles all interactions with collections of recommendations """
    @api.doc('create_recommendation')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(recommendation_model, code=201)
    def post(self):
        """
        Creates a Recommendation
        This endpoint will create a Recommendation based the data in the body that is posted
        """
        app.logger.info("Request to create a recommendation")
        check_content_type("application/json")
        recommendation = Recommendation()

        if not len(request.get_json()) > 0:
            return "", status.HTTP_400_BAD_REQUEST

        recommendation.deserialize(request.get_json())
        is_duplicate = Recommendation.check_if_duplicate(
            recommendation.product_1, recommendation.product_2)
        if is_duplicate:
            app.logger.info(
                "Recommendation with products [%s] and [%s] already exists.",
                recommendation.product_1, recommendation.product_2)
            abort(status.HTTP_406_NOT_ACCEPTABLE, "Recommendation with products" +
                  "'{recommendation.product_1}' and '{recommendation.product_1}'  already exists.")
        recommendation.create()
        location_url = api.url_for(RecommendationResource,
                                   recommendation_id=recommendation.id, _external=True)
        app.logger.info(
            "Recommendation with ID [%s] created.", recommendation.id)
        return recommendation.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

    ######################################################################
    # LIST ALL Recommendations
    ######################################################################

    @api.doc('list_recommendations')
    @api.marshal_list_with(recommendation_model)
    def get(self):
        """Returns all of the Recommendations"""
        app.logger.info("Request for recommendations list")
        recommendations = []
        category = request.args.get("recommendation_type")
        product_1 = request.args.get("product_1")
        product_2 = request.args.get("product_2")
        if category:
            recommendations = Recommendation.find_by_category(category)
        elif product_1:
            recommendations = Recommendation.find_by_product_1(product_1)
        elif product_2:
            recommendations = Recommendation.find_by_product_2(product_2)
        else:
            recommendations = Recommendation.all()

        results = [recommendation.serialize()
                   for recommendation in recommendations]
        app.logger.info("Returning %d recommendations", len(results))
        return results, status.HTTP_200_OK


######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route('/recommendations/<recommendation_id>')
@api.param('recommendation_id', 'The Recommendation identifier')
class RecommendationResource(Resource):
    """
    RecommendationResource class
    Allows the manipulation of an single recommendation
    GET /recommendations/{id} - Returns an recommendation with the id
    """
    ######################################################################
    # READ A Recommendation
    ######################################################################
    @api.doc('list_recommendation')
    @api.response(404, 'Recommendation not found')
    @api.marshal_with(recommendation_model)
    def get(self, recommendation_id):
        """Returns a Recommendation requested by it's ID"""
        app.logger.info("Request for a recommendation id=%s",
                        recommendation_id)
        recommendation = Recommendation.find(recommendation_id)
        if recommendation is None:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Recommendation with id '{recommendation_id}' was not found.")
        result = recommendation.serialize()
        app.logger.info(
            "Recommendation with ID [%s] has been read", recommendation.id)
        return result, status.HTTP_200_OK

    ######################################################################
    # UPDATE AN EXISTING RECOMMENDATION
    ######################################################################

    @api.doc('update_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.response(400, 'The posted Recommendation data was not valid')
    @api.expect(recommendation_model)
    @api.marshal_with(recommendation_model)
    def put(self, recommendation_id):
        """
        Update a Recommendation

        This endpoint will update a Recommendation based the body that is posted
        """
        app.logger.info(
            "Request to update recommendation with id: %s", recommendation_id)

        recommendation = Recommendation.find(recommendation_id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Recommendation with id '{recommendation_id}' was not found.")

        recommendation.deserialize(request.get_json())
        recommendation.id = recommendation_id
        recommendation.update()

        app.logger.info(
            "Recommendation with ID [%s] updated.", recommendation.id)
        return recommendation.serialize(), status.HTTP_200_OK

    ######################################################################
    # DELETE A RECOMMENDATION
    ######################################################################

    @api.doc('delete_recommendations')
    @api.response(204, 'Recommendation deleted')
    @api.response(404, 'Recommendation not found')
    def delete(self, recommendation_id):
        """
        Delete a recommendation
        This endpoint will delete a Recommendation based the id specified in the path
        """
        app.logger.info(
            "Request to delete Recommendation with id: %s", recommendation_id)
        recommendation = Recommendation.find(recommendation_id)
        if recommendation:
            recommendation.delete()

        app.logger.info(
            "Recommendation_id with ID [%s] delete complete.", recommendation_id)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /recommendations/{id}/like
######################################################################
@api.route('/recommendations/<recommendation_id>/like')
@api.param('recommendation_id', 'The Recommendation identifier')
class LikeRecommendation(Resource):
    """ Like actions on a Recommendation """
    ######################################################################
    # LIKE A RECOMMENDATION
    ######################################################################
    @api.doc('like_recommendations')
    @api.response(404, 'Recommendation not found')
    def put(self, recommendation_id):
        """
        Like a Recommendation

        This endpoint will liked a Recommendation given the recommendation ID
        """
        app.logger.info(
            "Request to like recommendation with id: %s", recommendation_id)

        recommendation = Recommendation.find(recommendation_id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Recommendation with id '{recommendation_id}' was not found.")

        recommendation.liked = True
        recommendation.update()

        app.logger.info(
            "Recommendation with ID [%s] liked.", recommendation.id)
        return recommendation.serialize(), status.HTTP_200_OK

    ######################################################################
    # DISLIKE A RECOMMENDATION
    ######################################################################

    @api.doc('dislike_recommendations')
    @api.response(404, 'Recommendation not found')
    def delete(self, recommendation_id):
        """
        Dislike a Recommendation

        This endpoint will dislike a Recommendation given the recommendation ID
        """
        app.logger.info(
            "Request to dislike recommendation with id: %s", recommendation_id)

        recommendation = Recommendation.find(recommendation_id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Recommendation with id '{recommendation_id}' was not found.")

        recommendation.liked = False
        recommendation.update()

        app.logger.info(
            "Recommendation with ID [%s] disliked.", recommendation.id)
        return recommendation.serialize(), status.HTTP_200_OK
