"""
Test cases for Recommendation Model

Test cases can be run with:
    nosetests
    coverage report -m

"""
import os
import logging
import unittest
from service import app
# from tests.factories import PetFactory
from service.models import Recommendation, RecommendationType, DataValidationError, db
from tests.factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestRecommendationModel(unittest.TestCase):
    """ Test Cases for Recommendation Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Recommendation.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_recommendation(self):
        """It should Create a test_create_a_recommendation and assert that it exists"""
        recommendation = Recommendation(
            product_1="aa", product_2="bb", recommendation_type=RecommendationType.CROSS_SELL)
        self.assertEqual(str(recommendation),
                         "<Recommendation aa and bb id=[None]>")
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.product_1, "aa")
        self.assertEqual(recommendation.product_2, "bb")
        self.assertEqual(recommendation.recommendation_type,
                         RecommendationType.CROSS_SELL)
        self.assertEqual(recommendation.liked, None)
        recommendation = Recommendation(
            product_1="aa", product_2="bb", recommendation_type=RecommendationType.UP_SELL)
        self.assertEqual(recommendation.recommendation_type,
                         RecommendationType.UP_SELL)
        recommendation = Recommendation(
            product_1="aa", product_2="bb", recommendation_type=RecommendationType.ACCESSORY)
        self.assertEqual(recommendation.recommendation_type,
                         RecommendationType.ACCESSORY)

    def test_add_a_recommendation(self):
        """It should Create a recommendation and add it to the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        recommendation = Recommendation(
            product_1="aa", product_2="bb", recommendation_type=RecommendationType.CROSS_SELL)
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        recommendation.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(recommendation.id)
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)

    def test_read_a_recommendation(self):
        """It should Read a recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        # Fetch it back
        found_rec = Recommendation.find(recommendation.id)
        self.assertEqual(found_rec.id, recommendation.id)
        self.assertEqual(found_rec.product_1, recommendation.product_1)
        self.assertEqual(found_rec.product_2, recommendation.product_2)
        self.assertEqual(found_rec.recommendation_type,
                         recommendation.recommendation_type)

    def test_update_a_recommendation(self):
        """It should Update a recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        logging.debug(recommendation)
        self.assertIsNotNone(recommendation.id)
        # Change it an save it
        recommendation.product_2 = "f2"
        original_id = recommendation.id
        recommendation.update()
        self.assertEqual(recommendation.id, original_id)
        self.assertEqual(recommendation.product_2, "f2")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].id, original_id)
        self.assertEqual(recommendations[0].product_2, "f2")

    def test_update_no_id(self):
        """It should not Update a recommendation with no id"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        self.assertRaises(DataValidationError, recommendation.update)

    def test_delete_a_recommendation(self):
        """It should Delete a recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertEqual(len(Recommendation.all()), 1)
        # delete the recommendation and make sure it isn't in the database
        recommendation.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_list_all_recommendations(self):
        """It should List all recommendations in the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        # Create 5 recommendations
        for _ in range(5):
            recommendation = RecommendationFactory()
            recommendation.create()
        # See if we get back 5 pets
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 5)

    def test_find_by_category(self):
        """It should Find recommendations by Category"""
        recommendations = RecommendationFactory.create_batch(10)
        for recommendation in recommendations:
            recommendation.create()
        category = recommendations[0].recommendation_type
        count = len([recommendation
                     for recommendation in recommendations
                     if recommendation.recommendation_type == category])
        found = Recommendation.find_by_category(category)
        self.assertEqual(found.count(), count)
        for recommendation in found:
            self.assertEqual(recommendation.recommendation_type, category)

    def test_find_by_product(self):
        """It should Find recommendations by product"""
        recommendations = RecommendationFactory.create_batch(10)
        for recommendation in recommendations:
            recommendation.create()
        product = recommendations[0].product_1
        count = len([recommendation for recommendation in recommendations if (
            product in (recommendation.product_1, recommendation.product_2))])
        found = Recommendation.find_by_product(product)
        self.assertEqual(found.count(), count)
        for recommendation in found:
            self.assertEqual(recommendation.product_1, product)

    def test_check_if_duplicate(self):
        """It should check if a recommendation already exists with the given products"""
        recommendations = RecommendationFactory.create_batch(5)
        for recommendation in recommendations:
            recommendation.create()
        recommendation = recommendations[0]
        product_1 = recommendation.product_1
        product_2 = recommendation.product_2
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 5)
        self.assertEqual(Recommendation.check_if_duplicate(
            product_1, product_2), True)
