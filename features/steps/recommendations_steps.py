"""
Recommendation Steps
Steps file for recommendations.feature
"""
import requests
from behave import given
from compare import expect


@given('the following recommendations')
def step_impl(context):
    """ Delete all recommendations and load new ones """
    # List all of the recommendations and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/api/recommendations"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for recommendation in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{recommendation['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new recommendations
    for row in context.table:
        payload = {
            "id": 0,
            "product_1": row['product_1'],
            "product_2": row['product_2'],
            "liked": row['liked'] in ['True', 'true', '1'],
            "recommendation_type": row['recommendation_type']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
