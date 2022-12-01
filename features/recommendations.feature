Feature: The recommendations service back-end
    As a User of the application
    I need a RESTful recommendations service
    So that I can keep track of all the recommendations

Background:
    Given the following recommendations
        | product_1       | product_2 | liked | recommendation_type  |
        | phone       | charger      | True      | UP_SELL    |
        | onion      | tomato      | True      | CROSS_SELL  |
        | brush        | paste     | False     | ACCESSORY    |
        | paint      | brush    | True      | UNKNOWN |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Recommendations Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "test 1"
    And I set the "product_2" to "test 2"
    And I select "False" in the "liked" dropdown
    And I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "test 1" in the "product_1" field
    And I should see "test 2" in the "product_2" field
    And I should see "False" in the "liked" dropdown
    And I should see "Cross Sell" in the "recommendation_type" dropdown

Scenario: Read a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "test 1"
    And I set the "product_2" to "test 2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "test 1" in the "product_1" field
    And I should see "test 2" in the "product_2" field
    And I should see "True" in the "liked" dropdown
    And I should see "Unknown" in the "recommendation_type" dropdown

Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "test 1"
    And I set the "product_2" to "test 2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "test 1" in the "product_1" field
    And I should see "test 2" in the "product_2" field
    And I should see "True" in the "liked" dropdown
    And I should see "Unknown" in the "recommendation_type" dropdown
    When I select "False" in the "liked" dropdown
    When I select "Up Sell" in the "recommendation_type" dropdown
    And I press the "Update" button
    And I press the "Clear" button
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "test 1" in the "product_1" field
    And I should see "test 2" in the "product_2" field
    And I should see "False" in the "liked" dropdown
    And I should see "Up Sell" in the "recommendation_type" dropdown
