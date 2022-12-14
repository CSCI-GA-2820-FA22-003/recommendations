# NYU DevOps - Recommendations 

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA22-003/recommendations/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/recommendations/actions)
[![codecov](https://codecov.io/github/CSCI-GA-2820-FA22-003/recommendations/branch/master/graph/badge.svg?token=47AVM4J6V4)](https://codecov.io/github/CSCI-GA-2820-FA22-003/recommendations)


## Overview :memo:

This project is a REST API service for recommendations. Each recommendation consists of product 1, product 2, type of recommendation, liked/disliked status.

## Setup :hammer_and_wrench:
:warning: Ensure Docker is installed and running :warning: 

Clone the repository
``` 
git clone https://github.com/CSCI-GA-2820-FA22-003/recommendations.git
``` 

Open project in VSCode
```
cd recommendations
code .
```

Select ```Reopen in Container```

Start the Service

``` 
honcho start 
``` 

## Links :round_pushpin:

Devlopment: 
```
http://169.51.206.138:31001/
```

Production: 
```
http://169.51.206.138:31002/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```


## Running Tests :wrench:

Running Unit Tests:
```
nosetests
```
Running BDD Tests
```
behave
```
:warning: Ensure the service is running before running ```behave``` :warning:
## Endpoints :green_circle:


```GET``` **/recommendations/healthcheck**

<i>Gives the health.</i>

Response Body:
```
{
    "message": "Healthy",
    "status": 200
}

```
---
```POST``` **/recommendations**

<i>Creates a recommendation.</i>

Request Body: 
```
{
    "id": 0,
    "liked": False,
    "product_1": "Phone",
    "product_2": "Charger",
    "recommendation_type": "UP_SELL"
}
```
Response Body:
```
{
    "id": 872,
    "liked": False,
    "product_1": "Phone",
    "product_2": "Charger",
    "recommendation_type": "UP_SELL"
}
```
The created record is returned in the response.

---

```GET``` **/recommendations**

<i>Lists all the recommendation.</i>

Response Body:
```
[
    {
        "id": 841,
        "liked": False,
        "product_1": "Charger",
        "product_2": "Phone Case",
        "recommendation_type": "UP_SELL"
    }
]
```
An array of all the recommendations is returned in the response.

---
```PUT``` **/recommendations/{recommendation_id}**

<i>Updates the recommendation with the recommendation_id.</i>

Request Body: 
```
{
        "id": 872,
        "liked": True,
        "product_1": "TV",
        "product_2": "Monitor",
        "recommendation_type": "CROSS_SELL"
}
```
Response Body:
```
{
    "id": 872,
    "liked": true,
    "product_1": "TV",
    "product_2": "Monitor",
    "recommendation_type": "CROSS_SELL"
}
```
The updated recommendation is returned in the response.

---

```GET``` **/recommendations/{recommendation_id}**

<i>Reads the recommendation with the recommendation_id.</i>

Response Body:
```
{
    "id": 872
    "liked": true
    "product_1": "TV",
    "product_2": "Monitor",
    "recommendation_type": "CROSS_SELL"
}
```
The recommendation with the id as recommendation_id is returned in the response.

---

```DELETE``` **/recommendations/{recommendation_id}**

<i>Deletes the recommendation with the recommendation_id.</i>

Response Body:
```
204 
NO CONTENT
```

```204 NO CONTENT``` is returned if the recommendation is deleted or not present.

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
