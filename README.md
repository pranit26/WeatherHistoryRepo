
# WeatherAPIProject sample application

This application has API that takes in a Location (Latitude & Longitude) and Number of Days as Input, and returns back Historic Weather Data (Hourly Temperature, Precipitation and Cloud Cover) for those number of days in the Past.

Also it has APIs which are register the user with password, generate JWT token with expiry time, doen user authentication,provide authorised user an access to API.




## Setup

The first thing to do is to clone the repository:

$ git clone 

$ cd sample-django-app

Create a virtual environment to install dependencies in and activate it:

$ python3 -m venv myenv

$ source env/bin/activate

Then install the dependencies:

(myenv)$ pip install -r requirements.txt

Note the (myenv) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv.

Once pip has finished downloading the dependencies:

(myenv)$  cd WeatherAPIProject

(env)$ python manage.py runserver

And navigate to http://127.0.0.1:8000/weather/.
## Tech Stack

>Django

>Django Rest Framework
MySQL

Numpy
Openmeteo
Pandas
Cryptography

## Running Tests

To run tests, run the following command

```bash
  python3 manage.py test weather
```
