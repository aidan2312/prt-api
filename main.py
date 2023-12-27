from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from fetch import LightRail
import json
import requests
import logging
import onetimepad as otp

app = FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@app.get("/api/lrt/getstops", name="Get Light Rail Stops")
def get_stops():
    """
    Endpoint to retrieve information about light rail stops.

    Returns:
        JSONResponse: JSON containing information about light rail stops.
    
    Raises:
        HTTPException: If the geojson file is not found (HTTP 404).
    """
    json_path = 'data/stops_auth.geojson'
    try:
        with open(json_path, "r") as file:
            json_content = json.load(file)
            return JSONResponse(content=json_content, media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/api/lrt/getvehicles", name="Get Light Rail Vehicles")
def get_vehicles():
    """
    Endpoint to retrieve information about light rail vehicles.

    Returns:
        JSONResponse: JSON containing information about light rail vehicles.
    """
    return LightRail.getVehicleJSON()

@app.get("/api/lrt/prediction", name="Get Prediction")
def getPrediction(stpid: str):
    """
    Endpoint to get predictions for a specific light rail stop.

    Args:
        stpid (string): Stop ID(s) for which predictions are requested separated by comma.

    Returns:
        JSON: Prediction information for the specified stop.
    """
    return LightRail.getPredictionStop(stpid)

@app.get("/api/lrt/getroutes", name="Get Routes")
def getRoutes():
    """
    Endpoint to retrieve information about light rail routes.

    Returns:
        JSON: Information about light rail routes.
    """
    return LightRail.getRoutes()

@app.get("/api/lrt/getbulletins", name="Get Bulletins")
def getBulletins():
    """
    Endpoint to retrieve bulletins related to light rail.

    Returns:
        JSON: Bulletins related to light rail.
    """
    return LightRail.getBulletins()

@app.get("/api/parcels/getParcel", name="Get Parcel")
def getParcel(pin: str):
    """
    Endpoint to retrieve parcel information.

    Args:
        pin (string): Parcel ID.

    Returns:
        JSON: Parcel information.
    """
    parcelUrl = 'http://tools.wprdc.org/property-api/v1/parcels/' + pin
    response = requests.get(parcelUrl)
    logging.info(response)
    return response.json()


@app.get("/api/otp/encrypt", name="Encrypt Message")
def encrypt(msg: str, key: str):
    """
    Endpoint to encrypt a message using a one-time pad.

    Args:
        msg (string): Message to encrypt.
        key (string): Key to use for encryption.

    Returns:
        string: Encrypted message.
    """
    return otp.encrypt(msg, key)

@app.get("/api/otp/decrypt", name="Decrypt Message")
def decrypt(msg: str, key: str):
    """
    Endpoint to decrypt a message using a one-time pad.

    Args:
        msg (string): Message to decrypt.
        key (string): Key to use for decryption.

    Returns:
        string: Decrypted message.
    """
    return otp.decrypt(msg, key)