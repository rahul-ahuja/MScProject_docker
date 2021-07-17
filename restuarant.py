from geocode import getGeocodeLocation
import json
import httplib2
from datetime import datetime
import sys
import codecs
import random
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "placeholder"
foursquare_client_secret = "placeholder"

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	lat,lon = getGeocodeLocation(location)

	h = httplib2.Http()

	url = f"https://api.foursquare.com/v2/venues/search?ll={lat},{lon}&client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v=20200101&query={mealType}"
	responses = json.loads(h.request(url, 'GET')[1])
	venues = responses['response']['venues']
	venue_names = []

	for ven_idx in range(len(venues)):
		if len(venues[ven_idx]['categories']) > 0:
			venue_names.append(venues[ven_idx]['categories'][0]['name'])

	if len(venue_names) > 0:
		return random.choice(venue_names)
	else:
		return 'No venue'
