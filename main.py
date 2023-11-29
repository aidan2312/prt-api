from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from fetch import LightRail
import json

app = FastAPI()

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
