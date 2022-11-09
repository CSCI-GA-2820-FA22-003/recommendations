
"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.request import Request
from service import app
from service.models import db, init_db, Recommendation, DataValidationError
from service.common import status
from service.routes import check_content_type
from tests.factories import RecommendationFactory  # HTTP Status Codes
from service import models
from urllib.parse import quote_plus
from unittest.mock import Mock

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/recommendations"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.app.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        logging.debug("Test Recommendation: %s", len(recommendations))
        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        self.client = app.test_client()
        test_recommendation = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_recommendation.serialize())
        response = self.client.post("/recommendations", json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_recommendation = response.get_json()
        #self.assertEqual(new_recommendation["id"], test_recommendation.id)
        self.assertEqual(new_recommendation["product_1"], test_recommendation.product_1)
        self.assertEqual(new_recommendation["product_2"], test_recommendation.product_2)
        #self.assertEqual(new_recommendation["recommendation_type"], test_recommendation.recommendation_type)

    def test_health(self):
        """It should be healthy"""
        response = self.app.get("/healthcheck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    def test_get_recommendations_list(self):
        """It should Get a list of recommendations"""
        self._create_recommendations(5)
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_read_recommendation(self):
        """It should read a recommendation queried by its ID"""
        recommendation = self._create_recommendations(1)[0]
        response = self.app.get(BASE_URL + f"/{recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_query_recommendations_list_by_category(self):
        """It should Query recommendations by Category"""
        recommendations = self._create_recommendations(10)
        test_category = recommendations[0].recommendation_type
        category_recommendations = [recommendation for recommendation in recommendations if recommendation.recommendation_type == test_category]
        response = self.app.get(
            BASE_URL,
            query_string="recommendation_type="+test_category.name
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(category_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["recommendation_type"], test_category.name)
            
    def test_update_recommendation(self):
            """It should Update an existing recommendation"""
            # create a recommendation to update
            test_recommendation = RecommendationFactory()
            response = self.app.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            test_recommendation = response.get_json()

            # update the recommendation
            test_recommendation["liked"]= False
            logging.debug(test_recommendation)
            id = response.get_json()["id"]
            response = self.app.put(f"{BASE_URL}/{id}", json=test_recommendation)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            updated_recommendation = response.get_json()
            self.assertEqual(updated_recommendation["liked"], False)

    def test_like_recommendation(self):
            """It should Like an existing recommendation"""
            # create a recommendation to like
            test_recommendation = RecommendationFactory()
            response = self.app.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            test_recommendation = response.get_json()

            # like the recommendation
            logging.debug(test_recommendation)
            id = response.get_json()["id"]
            response = self.app.put(f"{BASE_URL}/{id}/like")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            liked_recommendation = response.get_json()
            self.assertEqual(liked_recommendation["liked"], True)


    def test_delete_recommendation(self):
        """It should Delete a Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
        response = self.app.delete(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
    
######################################################################
#  T E S T   S A D   P A T H S
######################################################################

    def test_update_recommendation_missing(self):
        """It should not update a Recommendation that doesn't exist in the DB"""
        response = self.app.put(f"{BASE_URL}/12345")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recommendation_no_content_type(self):
        """It should not Create a Recommendation with no content type"""
        response = self.app.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_recommendation_missing_content(self):
        """It should not Create a Recommendation with missing content type"""
        response = self.app.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_method_not_allowed(self):
        """It should not invoke endpoints with incorrect HTTP methods"""

        # Delete on Base URL
        response = self.app.delete(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Put on Base URL 
        response = self.app.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Recommendation with missing data"""
        data = {"id":"1"}
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)



    


    






