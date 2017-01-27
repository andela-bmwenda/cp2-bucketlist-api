[![Build Status](https://travis-ci.org/andela-bmwenda/cp2-bucketlist-api.svg?branch=master)](https://travis-ci.org/andela-bmwenda/cp2-bucketlist-api)[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f556e41f24c744e0a2a0cff938f59e5b)](https://www.codacy.com/app/boniface-mwenda/cp2-bucketlist-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-bmwenda/cp2-bucketlist-api&amp;utm_campaign=Badge_Grade)[![Coverage Status](https://coveralls.io/repos/github/andela-bmwenda/cp2-bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-bmwenda/cp2-bucketlist-api?branch=develop)

# Bucketlist API

## CONTENTS

 - Introduction
 - Requirements
 - Installation
 - Features
 - Testing
 - License
 
## Introduction
 
This is a flask api powered by [flask-restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/). This api has end points that allow the user to create, update, delete and get bucketlist entries. Also, users can also add items to particular bucketlists, and track their status by checking if they are done or not.

## Requirements
 
 Bucketlist api is a Flask application that utilises the flask-restful framework. The app has been tested for `python 3.5` and `python 3.6`. The app uses a sqlite3 database.
 
## Installation
 
Clone this repo using htts or ssh, depending on your preference.
 
 ssh:
>`$ git clone git@github.com:andela-bmwenda/cp2-bucketlist-api.git`

http:
>`$ git clone https://github.com/andela-bmwenda/cp2-bucketlist-api.git`

cd into the created folder and install a [virtual environment](https://virtualenv.pypa.io/en/stable/)

`$ virtualenv venv`

Activate the virtual environment

`$ venv/bin/activate`

Install all app requirements

`$ pip install -r requirements.txt`

Create the database and run migrations

`$ python manage.py db init`

`$ python manage.py db migrate`

`$ python manage.py db upgrade`

All done! Now, start your server by running `python manage.py runserver`. For best experience, use a GUI platform like [postman](https://www.getpostman.com/) to make requests to the api.

## Features

### Endpoints

Here is a list of all the endpoints in bucketlist app.

Endpoint | Functionality
------------ | -------------
POST /auth/login |Logs a user in
POST /auth/register | Registers a user
POST /bucketlists/ | Creates a new bucket list
GET /bucketlists/ | Lists all created bucket lists
GET /bucketlists/id | Gets a single bucket list with the suppled id 
PUT /bucketlists/id | Updates bucket list with the suppled id
DELETE /bucketlists/id | Deletes bucket list with the suppled id
POST /bucketlists/id/items/ | Creates a new item in bucket list
PUT /bucketlists/id/items/item_id | Updates a bucket list item
DELETE /bucketlists/id/items/item_id | Deletes an item in a bucket list

### Pagination

The api supports pagination by parsing a parameter `limit` in the GET request. By default, the api returns 20 items, and the maximum limit for results in each get request is 100.

Example

`GET http://localhost:/bucketlists?limit=30`

This returns 30 bucketlists records for the logged in user.

### Searching

It is possible to search bucketlists using the parameter `q` in the GET request. 
Example:

`GET http://localhost:/bucketlists?q=travel`

This request will return all bucketlists with `travel` in their name

### Sample GET response

Below is a sample of a GET request for bucketlist

```
{
  "name": "Sample buckelist"
  
  "created_by": "bender",
  
  "date_created": "Thu, 26 Jan 2017 20:28:00 GMT",
  
  "date_modified": "Thu, 26 Jan 2017 20:28:00 GMT",
  
  "id": 1,
  
  "items": [
  
    {
    
      "date_created": "2017-01-26T20:55:08.437672+00:00",
      
      "date_modified": "2017-01-26T20:55:08.437685+00:00",
      
      "done": false,
      
      "id": 1,
      
      "name": "Give a talk"
      
    },
    
    {
      "date_created": "2017-01-26T20:55:21.754565+00:00",
      
      "date_modified": "2017-01-26T20:55:21.754573+00:00",
      
      "done": false,
      
      "id": 2,
      
      "name": "Get mentor"
      
    },
    
    {
    
      "date_created": "2017-01-26T20:55:35.261938+00:00",
      
      "date_modified": "2017-01-26T20:55:35.261945+00:00",
      
      "done": false,
      
      "id": 3,
      
      "name": "Be awesome"
      
    }
    
  ]
  
}
```

## Testing

The application has been tested based on the [flask-testing](https://pythonhosted.org/Flask-Testing/) library. Tests can be run manually using test runners such as `nose` or `pytest`.
Example
To run tests with nose, run `nosetests`

## License

The API uses an MIT license








