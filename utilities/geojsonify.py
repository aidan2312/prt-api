import geojson
from shapely.geometry import Point, LineString, shape, mapping
from shapely.ops import nearest_points
import requests

#PRT's Light Rail Lines (just need to be geojson)
agol_lines = requests.get("https://services3.arcgis.com/544gNI3xxlFIWuTc/arcgis/rest/services/PAAC_Routes_current/FeatureServer/0/query?where=MODE+%3D+%27Light+Rail%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=").json()

#convert a stop to geojson
def stops_to_geojson(data):
    features = []

    for stop in data:
        lat = float(stop['lat'])
        lon = float(stop['lon'])
        properties = {
            'stpid': stop['stpid'],
            'stpnm': stop['stpnm'],
            'dir': stop['direction'],
            'line': stop['line']
        }

        feature = geojson.Feature(geometry=geojson.Point((lon, lat)), properties=properties)
        features.append(feature)

    return geojson.FeatureCollection(features)

#convert a vehicle to geojson
def vehicle_to_geojson(data):
    features = []
    
    for vehicle in data['bustime-response']['vehicle']:
        lat = float(vehicle['lat'])
        lon = float(vehicle['lon'])
        properties = {
            'des': vehicle['des'],
            'dly': vehicle['dly'],
            'hdg': vehicle['hdg'],
            'mode': vehicle['mode'],
            'origtatripno': vehicle['origtatripno'],
            'pdist': vehicle['pdist'],
            'pid': vehicle['pid'],
            'psgld': vehicle['psgld'],
            'rt': vehicle['rt'],
            'rtpidatafeed': vehicle['rtpidatafeed'],
            'spd': vehicle['spd'],
            'stsd': vehicle['stsd'],
            'stst': vehicle['stst'],
            'tablockid': vehicle['tablockid'],
            'tatripid': vehicle['tatripid'],
            'tmstmp': vehicle['tmstmp'],
            'vid': vehicle['vid'],
            'zone': vehicle['zone']
        }

        # Create a GeoJSON point feature
        point_feature = geojson.Feature(geometry=geojson.Point((lon, lat)), properties=properties)

        # Snap the point to the nearest line in agol_lines
        snap_to_nearest_line(point_feature['geometry'], agol_lines)

        features.append(point_feature)

    feature_collection = geojson.FeatureCollection(features)

    return feature_collection

def snap_to_nearest_line(point, lines):
    # Convert the point to a Shapely geometry
    point_geom = Point(point['coordinates'])

    # Find the nearest line in the list of lines
    nearest_line = None
    min_distance = float('inf')

    for line in lines['features']:
        line_geom = shape(line['geometry'])
        nearest = nearest_points(point_geom, line_geom)
        
        if nearest is not None:
            distance = nearest[0].distance(nearest[1])

            if distance < min_distance:
                min_distance = distance
                nearest_line = line

    if nearest_line is not None:
        # Snap the point to the nearest point on the nearest line
        nearest_point_on_line = nearest_points(point_geom, shape(nearest_line['geometry']))[1]

        # Update the point's coordinates with the snapped coordinates
        point['coordinates'] = mapping(nearest_point_on_line)['coordinates']

    return point

