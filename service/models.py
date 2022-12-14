"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Recommendation.init_db(app)

class DatabaseConnectionError(Exception):
    """ Used for data connection errors """

class DataValidationError(Exception):
    """ Used for data validation errors when deserializing """


class RecommendationType(Enum):
    """Enumeration of valid Recommendation Types"""

    CROSS_SELL = 0
    UP_SELL = 1
    ACCESSORY = 2
    UNKNOWN = 3


class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    product_1 = db.Column(db.String(63), nullable=False)
    product_2 = db.Column(db.String(63), nullable=False)
    recommendation_type = db.Column(
        db.Enum(RecommendationType), nullable=False,
        server_default=(RecommendationType.UNKNOWN.name)
    )
    liked = db.Column(db.Boolean())

    def __repr__(self):
        return f"<Recommendation {self.product_1} and {self.product_2} id=[{self.id}]>"

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating Recommendation for %s and %s",
                    self.product_1, self.product_2)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving Recommendation %s and %s",
                    self.product_1, self.product_2)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Recommendation from the data store """
        logger.info("Deleting Recommendation %s and %s",
                    self.product_1, self.product_2)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Recommendation into a dictionary """
        return {
            "id": self.id,
            "product_1": self.product_1,
            "product_2": self.product_2,
            "recommendation_type": self.recommendation_type.name,  # convert enum to string
            "liked": self.liked
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if not isinstance(data, dict):
                raise DataValidationError(
                    "Invalid Recommendation: body of request contained bad or no data - "
                    "Error message: " + "data type is not a dictionary"
                )

            self.product_1 = data["product_1"]
            self.product_2 = data["product_2"]
            self.recommendation_type = data["recommendation_type"]
            if isinstance(data["liked"], bool):
                self.liked = data["liked"]
            self.id = data["id"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Recommendation: missing " + error.args[0]
            )

        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Recommendation in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Recommendation by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Recommendations in a category
        :param category: the category of the Recommendations you want to match
        :type category: str
        :return: a collection of Recommendations in that category
        :rtype: list
        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.recommendation_type == category)

    @classmethod
    def find_by_product(cls, product: str) -> list:
        """Returns all of the Recommendations for a product
        :param category: the product for which you want to get the Recommendations
        :type product: str
        :return: a collection of products in that category
        :rtype: list
        """
        logger.info(
            "Processing product recommendations query for %s ...", product)
        return cls.query.filter(cls.product_1 == product)

    @classmethod
    def find_by_product_1(cls, product: str) -> list:
        """Returns all of the Recommendations for a product
        :param category: the product for which you want to get the Recommendations
        :type product: str
        :return: a collection of products in that category
        :rtype: list
        """
        logger.info(
            "Processing product recommendations query for %s ...", product)
        return cls.query.filter(cls.product_1 == product)

    @classmethod
    def find_by_product_2(cls, product: str) -> list:
        """Returns all of the Recommendations for a product
        :param category: the product for which you want to get the Recommendations
        :type product: str
        :return: a collection of products in that category
        :rtype: list
        """
        logger.info(
            "Processing product recommendations query for %s ...", product)
        return cls.query.filter(cls.product_2 == product)

    @classmethod
    def check_if_duplicate(cls, product_1: str, product_2: str) -> list:
        """Returns true if a recommendation already exists with the given products,
            else returns false
        :param product_1: the product_1 of the Recommendations
        :param product_2: the product_2 of the Recommendations
        :return: boolean
        """
        logger.info(
            "Checking if a recommendation already exists for %s and %s ...", product_1, product_2)
        return (cls.query
                .filter(cls.product_1 == product_1)
                .filter(cls.product_2 == product_2).count() > 0)
