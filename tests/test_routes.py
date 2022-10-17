
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
from service import app
from service.models import db
from service.common import status
from tests.factories import RecommendationFactory  # HTTP Status Codes
from service import models


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
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
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
        self.client = app.test_client()
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    def test_get_recommendations_list(self):
        """It should Get a list of recommendations"""
        self.client = app.test_client()
        self._create_recommendations(5)
        response = self.client.get("/recommendations/list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)


