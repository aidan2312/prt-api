
# PRT-API

 Second iteration of this project - migrated from Flask to FastAPI since I am no longer relying on Jinja templates and not including a client.  This API processes responses from a BusTime API and returns the data in easy-to-read (and locate), concise GeoJSON, allowing it to be easily integrated into any web map that supports GeoJSON.  
 

 You need an API Key to access the transit feeds.  Reach out to your transit provider for that.



## Authors

- [Aidan Donnelly (@aidan2312)](https://www.github.com/aidan2312)
## Installation

Clone this repo

```bash
  git clone https://github.com/aidan2312/prt-api
  cd prt-api
```
Install Python packages
```bash
  pip -r requirements.txt
```
Run the app
```bash
  uvicorn main:app --reload
```
Navigate to http://127.0.0.1:8000/docs 
## Demo

TBD


## License


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)



## Environment Variables
Since different transit authorities may categorize datafeeds in different ways, I've split up endpoints into the .env file, which must be in the root directory.

`API_KEY` = Your transit authority's BusTime API Key

`API_ROOT_URL` = Root url of the BusTime API you're fetching from (e.g. http://<Host>/bustime/api/v3/)

`STOPS_ENDPOINT` = The stops endpoint, typically /getstops/

`PREDICTIONS_ENDPOINT` = The predictions endpoint, typically /getpredictions/

`VEHICLE_ENDPOINT` = The vehicles endpoint, typically /getvehicles/

`PATTERNS_ENDPOINT` = The patterns endpoint, typically /getpatterns/

`SERVICE_BULLETINS_ENDPOINT` = service bulletins endpoint, varies by provider.

Example (this example works if you're in Pittsburgh, just get an API key): 


```
API_KEY="asdtasdfasdrewasdf"
API_ROOT_URL="http://truetime.portauthority.org/bustime/api/v3/"
STOPS_ENDPOINT="getstops"
PREDICTIONS_ENDPOINT="getpredictions"
VEHICLE_ENDPOINT="getvehicles"
PATTERNS_ENDPOINT="getpatterns"
SERVICE_BULLETINS_ENDPOINT="getservicebulletins"

```




## Documentation

[BusTime Docs](https://realtime.ridemcts.com/bustime/apidoc/docs/DeveloperAPIGuide3_0.pdf)

