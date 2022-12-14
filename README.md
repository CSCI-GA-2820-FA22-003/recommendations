# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA22-003/recommendations/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/recommendations/actions)
[![codecov](https://codecov.io/github/CSCI-GA-2820-FA22-003/recommendations/branch/master/graph/badge.svg?token=47AVM4J6V4)](https://codecov.io/github/CSCI-GA-2820-FA22-003/recommendations)


This is a skeleton you can use to start your projects

## Overview

This project is a REST API service for recommendations. Each recommendation consists of product 1, product 2, type of recommendation, liked/disliked status.

## Setup

Use ``` git clone https://github.com/CSCI-GA-2820-FA22-003/recommendations.git``` to clone the repository in your local machine.

Start the docker desktop, open the code in VSCode and click ```Reopen in Container```.

And then, ``` honcho start ``` to start the flask server.

## Endpoints

Devlopment Enviroment: http://169.51.206.138:31001/

Production Enviroment: http://169.51.206.138:31002/

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


## Running and testing Instructions

Run the server on cmd by using the command flask run and for tetsing use nosetests and postman.

## Endpoints


**GET /recommendations/healthcheck:**

<i>Gives the health.</i>

Response Body:<br/>

{<br/>
    "message": "Healthy",<br/>
    "status": 200<br/>
}

<br/>
<br/>

**POST /recommendations :**

<i>Creates a recommendation.</i>

Request Body: <br/>
{<br/>
        "id": 0,<br/>
        "liked": false,<br/>
        "product_1": "aaaa",<br/>
        "product_2": "bbbb",<br/>
        "recommendation_type": "UP_SELL"<br/>
}

Response Body:<br/>
{<br/>
    "id": 872,<br/>
    "liked": false,<br/>
    "product_1": "aaaa",<br/>
    "product_2": "bbbb",<br/>
    "recommendation_type": "UP_SELL"<br/>
}

The created record is returned in the response.

<br/>
<br/>

**GET /recommendations :**

<i>Lists all the recommendation.</i>

Response Body:<br/>

[<br/>
    {<br/>
        "id": 841,<br/>
        "liked": false,<br/>
        "product_1": "a1",<br/>
        "product_2": "d2",<br/>
        "recommendation_type": "UP_SELL"<br/>
    }<br/>
]

An array of all the recommendations is returned in the response.

<br/>
<br/>

**PUT /recommendations/{recommendation_id} :**

<i>Updates the recommendation with the recommendation_id.</i>

Request Body: <br/>
{<br/>
        "id": 872,<br/>
        "liked": true,<br/>
        "product_1": "aaaa",<br/>
        "product_2": "bbbb",<br/>
        "recommendation_type": "CROSS_SELL"<br/>
}

Response Body:<br/>
{<br/>
    "id": 872,<br/>
    "liked": true,<br/>
    "product_1": "aaaa",<br/>
    "product_2": "bbbb",<br/>
    "recommendation_type": "CROSS_SELL"<br/>
}

The updated recommendation is returned in the response.

<br/>
<br/>

**GET /recommendations/{recommendation_id} :**

<i>Reads the recommendation with the recommendation_id.</i>

Response Body ( GET http://localhost:8080/recommendations/872 ):<br/>
{<br/>
    "id": 872,<br/>
    "liked": true,<br/>
    "product_1": "aaaa",<br/>
    "product_2": "bbbb",<br/>
    "recommendation_type": "CROSS_SELL"<br/>
}

The recommendation with the id as recommendation_id is returned in the response.

<br/>
<br/>

**DELETE /recommendations/{recommendation_id} :**

<i>Deletes the recommendation with the recommendation_id.</i>

Response Body ( DELETE http://localhost:8080/recommendations/872 ):<br/>
204NO CONTENT

204 NO CONTENT is returned if the recommendation is delted or not present.

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
