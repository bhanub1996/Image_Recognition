import mapbox
import json
import responses

def mapbox_reverse(lat, lon):
    print((lat,lon))    
    body = json.dumps({"query": [lon, lat]})    
    token = "pk.eyJ1IjoiZ2hvdXNlcyIsImEiOiJjbGZnbjBscjAwcHBpM3RvOTdxYndqdTB4In0.-xhYjOzdVy7eAIl3wNrFog"    
    responses.add(responses.GET,'https://api.mapbox.com/geocoding/v5/mapbox.places/{lon},{lat}.json?access_token={token}',match_querystring=True, body=body,status=200,content_type='application/json')    
    response = mapbox.Geocoder(access_token=token).reverse(lon=lon, lat=lat)    
    # print(response.json()['features'][0]['place_name'])    
    return response.json()

def mapbox_forward(search_text):
    
    token = "pk.eyJ1IjoiZ2hvdXNlcyIsImEiOiJjbGZnbjBscjAwcHBpM3RvOTdxYndqdTB4In0.-xhYjOzdVy7eAIl3wNrFog"    
    responses.add(responses.GET,'https://api.mapbox.com/geocoding/v5/mapbox.places/{search_text}.json?access_token={token}',match_querystring=True,status=200,content_type='application/json')    
    response = mapbox.Geocoder(access_token=token).forward(address=search_text)   
    # print(response.json()['features'][0]['place_name'])    
    return response.json()

# https://api.mapbox.com/geocoding/v5/{endpoint}/{search_text}.json