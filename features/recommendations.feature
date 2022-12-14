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

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "phone" in the results
    And I should see "brush" in the results
    And I should not see "apple" in the results

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
    
    
Scenario: Delete a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "product one"
    And I set the "product_2" to "product two"
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
    And I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Not Found!"
    And the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty


Scenario: Like a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "product one"
    And I set the "product_2" to "product two"
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
    And I press the "Like" button
    Then I should see the message "Recommendation liked!"
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "product one" in the "product_1" field
    And I should see "product two" in the "product_2" field
    And I should see "True" in the "liked" dropdown


Scenario: Dislike a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "p1"
    And I set the "product_2" to "p2"
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
    And I press the "Dislike" button
    Then I should see the message "Recommendation disliked!"
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "p1" in the "product_1" field
    And I should see "p2" in the "product_2" field
    And I should see "False" in the "liked" dropdown


Scenario: Search by Category
    When I visit the "Home Page"
    And I set the "product_1" to "tomato"
    And I set the "product_2" to "potato"
    And I select "False" in the "liked" dropdown
    And I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Search" button
    Then I should see "onion" in the "product_1" field
    And I should see "tomato" in the "product_2" field
    And I should see "True" in the "liked" dropdown
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Search" button
    Then I should see "tomato" in the "product_1" field
    And I should see "potato" in the "product_2" field
    And I should see "False" in the "liked" dropdown
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Search" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty


Scenario: Search by Product 1
    When I visit the "Home Page"
    And I set the "product_1" to "phone"
    And I set the "product_2" to "laptop"
    And I select "True" in the "liked" dropdown
    And I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I set the "product_1" to "phone"
    And I press the "Search" button    
    Then I should see the message "Success"
    Then I should see "phone" in the "product_1" field
    And I should see "charger" in the "product_2" field
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I set the "product_1" to "phone"
    And I press the "Search" button
    Then I should see the message "Success"
    Then I should see "phone" in the "product_1" field
    And I should see "laptop" in the "product_2" field
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I set the "product_1" to "phone"
    And I press the "Search" button
    Then I should see the message "Success"
    Then the "id" field should be empty
    And the "product_2" field should be empty



Scenario: Search by Product 2
    When I visit the "Home Page"
    And I set the "product_1" to "laptop"
    And I set the "product_2" to "charger"
    And I select "True" in the "liked" dropdown
    And I select "Cross Sell" in the "recommendation_type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    Then the "id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    When I set the "product_2" to "charger"
    And I press the "Search" button    
    Then I should see the message "Success"
    Then I should see "phone" in the "product_1" field
    And I should see "charger" in the "product_2" field
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I set the "product_2" to "charger"
    And I press the "Search" button
    Then I should see the message "Success"
    Then I should see "laptop" in the "product_1" field
    And I should see "charger" in the "product_2" field
    When I press the "Delete" button
    Then I should see the message "Recommendation has been Deleted!"
    When I set the "product_2" to "charger"
    And I press the "Search" button
    Then I should see the message "Success"
    Then the "id" field should be empty
    And the "product_1" field should be empty