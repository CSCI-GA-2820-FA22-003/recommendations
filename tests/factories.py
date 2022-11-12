"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake Recommendations that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    id = factory.Sequence(lambda n: n)
    #using sequence to generate unique recommendations each time
    product_1 = factory.Sequence(lambda n: f"a_{n}")
    product_2 = factory.Sequence(lambda n: f"b_{n}")
    recommendation_type = FuzzyChoice(choices=[RecommendationType.CROSS_SELL, 
        RecommendationType.UP_SELL, RecommendationType.ACCESSORY])