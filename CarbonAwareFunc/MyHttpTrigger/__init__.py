# Creata a function  that mimics turning on industrial equipement if the Carbon intensity of the UK Grid less than 100gCO2/kWh
# I am getting the carbon intensity from the National Grid Carbon Intensity API at https://api.carbonintensity.org.uk/
# The api above returns this json data:
# {
#     "data": [
#         {
#             "from": "2023-07-20T09:30Z",
#             "to": "2023-07-20T10:00Z",
#             "intensity": {
#                 "forecast": 179,
#                 "actual": 187,
#                 "index": "moderate"
#             }
#         }
#     ]
# }
# I want to use the request libary to get the data from the api and then use the json libary to parse the data
# the response should be a json block with a key of "ShouldTurnOn" and a value of true or false
# I will then use the requests libary to post the json data to a http endpoint

import logging
import json
import requests

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get the carbon intensity data from the API
    response = requests.get("https://api.carbonintensity.org.uk/intensity")
    data = response.json()
    # get the actual carbon intensity from the json
    actual = data["data"][0]["intensity"]["actual"]
    # get the forecast carbon intensity from the json
    forecast = data["data"][0]["intensity"]["forecast"]
    # check if the actual carbon intensity is less than 100gCO2/kWh
    if actual < 100:
        # create a json block with a key of "ShouldTurnOn" and a value of true
        json_block = {"ShouldTurnOn": "true"}
    else:
        # create a json block with a key of "ShouldTurnOn" and a value of false
        json_block = {"ShouldTurnOn": "false"}
    # post the json data to the http endpoint
    response = requests.post("https://webhook.site/2c2c4d6a-3d2f-4f4f-ba2a-9c5c2c0f2d2d", json=json_block)

    return func.HttpResponse(
        json.dumps(json_block),
        status_code=200
    )


    
