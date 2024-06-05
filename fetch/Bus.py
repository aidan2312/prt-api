from dotenv import load_dotenv
import os
from pathlib import Path
import requests
import geojson
from utilities import geojsonify

load_dotenv()
dotenv_path = Path('./.env')
API_KEY = os.getenv("API_KEY")
API_ROOT_URL=os.getenv("API_ROOT_URL")
STOPS_ENDPOINT=os.getenv("STOPS_ENDPOINT")
PREDICTIONS_ENDPOINT=os.getenv("PREDICTIONS_ENDPOINT")
VEHICLE_ENDPOINT=os.getenv("VEHICLE_ENDPOINT")
PATTERNS_ENDPOINT=os.getenv("PATTERNS_ENDPOINT")
SERVICE_BULLETINS_ENDPOINT=os.getenv("SERVICE_BULLETINS_ENDPOINT")

BASE_PARAMS = {
    'key': API_KEY,
    'format': 'json',
    'rtpidatafeed': 'Port Authority Bus'
}


stops_url = f'{API_ROOT_URL}{STOPS_ENDPOINT}'
vehicles_url = f'{API_ROOT_URL}{VEHICLE_ENDPOINT}'
patterns_url = f'{API_ROOT_URL}{PATTERNS_ENDPOINT}'
predictions_url = f'{API_ROOT_URL}{PREDICTIONS_ENDPOINT}'

agol_lines = requests.get("https://services3.arcgis.com/544gNI3xxlFIWuTc/arcgis/rest/services/PAAC_Routes_current/FeatureServer/0/query?where=MODE+%3D+%27Light+Rail%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=").json()

line_direction = {
    
    'RED': ['INBOUND', 'OUTBOUND'],
    'SLVR': ['INBOUND', 'OUTBOUND'],
    'BLUE': ['INBOUND', 'OUTBOUND']
}


# FETCH VEHICLES
def getVehicleJSON():
    vehicle_params = {
        **BASE_PARAMS,
        'rt': "BLUE,RED,SLVR"
    }

    response = requests.get(vehicles_url, params=vehicle_params)
    return geojsonify.vehicle_to_geojson(response.json())

# END FETCH VEHICLES

#FETCH PREDICTIONS
def getPredictionStop(stpid):
    predictions = ""
    prediction_params = {
        **BASE_PARAMS,
        'stpid': stpid,
        'top': 15

    }

    
    predictions = requests.get(predictions_url, params=prediction_params).json()["bustime-response"]
    return predictions



# END FETCH PREDICTIONS

#FETCH ROUTES
def getRoutes():
    return requests.get("https://services3.arcgis.com/544gNI3xxlFIWuTc/arcgis/rest/services/PAAC_Routes_current/FeatureServer/0/query?where=MODE+%3D+%27Light+Rail%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=").json()

# END FETCH ROUTES

# FETCH BULLETINS
def getBulletins():
    service_bulletin_params = {
        **BASE_PARAMS,
        'rt': "BLUE,RED,SLVR"
    }
    
    response = requests.get(API_ROOT_URL + SERVICE_BULLETINS_ENDPOINT, params=service_bulletin_params).json()['bustime-response']['sb']
    
    return response


