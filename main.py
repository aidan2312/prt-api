from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from fetch import LightRail
import json
app = FastAPI()




@app.get("/api/lrt/getstops")
def get_stops():
    json_path = 'data/stops_auth.geojson'
    try:
        with open(json_path, "r") as file:
            json_content = json.load(file)
            return JSONResponse(content=json_content, media_type="application/json")
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="File not found")
    

@app.get("/api/lrt/getvehicles")
def get_vehicles():
    return LightRail.getVehicleJSON()

@app.get("/api/lrt/prediction")
def getPrediction(stpid: str):
    return LightRail.getPredictionStop(stpid)

@app.get("/api/lrt/getroutes")
def getRoutes():
    return LightRail.getRoutes()

@app.get("/api/lrt/getbulletins")
def getBulletins():
    return LightRail.getBulletins()