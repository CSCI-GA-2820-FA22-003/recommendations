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
    product_1 = FuzzyChoice(choices=["a1", "b1", "c1", "d1"])
    product_2 = FuzzyChoice(choices=["a2", "b2", "c2", "d2"])
    recommendation_type = FuzzyChoice(choices=[RecommendationType.CROSS_SELL, 
        RecommendationType.UP_SELL, RecommendationType.ACCESSORY])