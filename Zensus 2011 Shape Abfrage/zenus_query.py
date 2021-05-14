import json
import easygui
import urllib.request
import urllib.parse

filename = easygui.fileopenbox(filetypes=["*.json"], title="Quell-GeoJSON auswählen", multiple=False)
raw_geojson = ""
with open(filename, 'r') as json_file:
	raw_geojson = json.load(json_file)
	
zensus_url = "https://www.gis-rest.nrw.de/grs/rest/statistik/zensus_2011/einwohner_sum.json"

crs_value = raw_geojson["crs"]
polygons = raw_geojson["features"]

for i, polygon in enumerate(polygons):
	einwohner = 0
	grid = 0
	polygon["crs"] = crs_value
	try:
		# Aus irgend einem Grund hält die Webseite sehr stark daran fest Double-Quotes zu haben
		htmlified_polygon = urllib.parse.quote(str(polygon).replace("'",'"'))
		url = zensus_url + "?data=" + htmlified_polygon
		result = urllib.request.urlopen(url).read()
		json_results = json.loads(result.decode())
		einwohner = json_results["properties"]["einwohner"]
		grid = json_results["properties"]["grid"]
	except urllib.error.HTTPError:
		message = "Ein Fehler ist aufgetreten. Möglicherweise hat das Polygon %i zu viele Koordinaten. \n In dem Polygon sind %i Koordinaten. Die zusätzlichen Daten des Polygons werden auf 0 gesetzt" % (i, len(polygon["geometry"]["coordinates"][0]))
		easygui.msgbox(msg=message)
	polygon["properties"]["einwohner"] = einwohner
	polygon["properties"]["grid"] = grid
	polygon.pop("crs", None)
	
outfile = easygui.filesavebox("Zieldatei auswählen", default="target.json", filetypes='\*.json')
with open(outfile, 'w') as out:
	json.dump(raw_geojson, out)