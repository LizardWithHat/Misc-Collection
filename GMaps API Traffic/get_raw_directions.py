import googlemaps
import argparse
import json
import datetime

#TODO: work with functions

#neccessary arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("origin", help="LAT,LONG of starting point")
argparser.add_argument("destination", help="LAT,LONG of destination point")

#optional arguments
argparser.add_argument("-V", "--via", action="append", help="waypoints (LAT,LONG) that have to be traveled through, can be used multiple times and will be used in given order")
argparser.add_argument("-D", "--departure_time", help="specify the departure time as int in seconds from Jan 1st 1970. Default is current time", default='now')
argparser.add_argument("-o", "--outputfile", help="where to parse the received raw data")

args = argparser.parse_args()

via_waypoints = ""
if args.via:
	for point in args.via:
		via_waypoints += "via:" + point + "|"
	via_waypoints = via_waypoints[:-1]
	
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXX"

#Must use directions instead of distance_matrix API, otherwise we can't specify waypoints
gmaps = googlemaps.Client(key=api_key)
directions_result = gmaps.directions(args.origin,
	args.destination,
	departure_time = args.departure_time,
	units = "metric",
	mode = "driving",
	waypoints = via_waypoints,
	language="de")

#Write output to given file
if args.outputfile:
	raw_json = json.dumps(directions_result, sort_keys=True, indent=4)
	with open(args.outputfile, "w") as file:
		file.write(raw_json)

#Assemble CSV Line and output
#Expected CSV Header: Timestamp, Start Address, Start Location Latitude, Start Location Longitude, End Address, End Location Latitude, End Location Longitude, Distance, Distance in Words, Time, Time in Words, Time in Traffic, Time in Traffic in Words, Summary, Warnings, Copyrights
#Working Task-Scheduler line to append to a CSV-File (Example):
# in a script file: & "python.exe" "<PATH>\get_raw_directions.py" 51.508114,7.465302 51.437627,7.570480 -V 51.504208,7.517991 >> "FILE.csv"
delimiter = ";"
csvline = str(datetime.datetime.now()) + delimiter
csvline += directions_result[0]['legs'][0]['start_address'] + delimiter
csvline += str(directions_result[0]['legs'][0]['start_location']['lat']) + delimiter
csvline += str(directions_result[0]['legs'][0]['start_location']['lng']) + delimiter
csvline += directions_result[0]['legs'][0]['end_address'] + delimiter
csvline += str(directions_result[0]['legs'][0]['end_location']['lat']) + delimiter
csvline += str(directions_result[0]['legs'][0]['end_location']['lng']) + delimiter
csvline += str(directions_result[0]['legs'][0]['distance']['value']) + delimiter
csvline += directions_result[0]['legs'][0]['distance']['text'] + delimiter
csvline += str(directions_result[0]['legs'][0]['duration']['value']) + delimiter
csvline += directions_result[0]['legs'][0]['duration']['text'] + delimiter
csvline += str(directions_result[0]['legs'][0]['duration_in_traffic']['value']) + delimiter
csvline += directions_result[0]['legs'][0]['duration_in_traffic']['text'] + delimiter
csvline += directions_result[0]['summary'] + delimiter
csvline += str(directions_result[0]['warnings'])[1:-1] + delimiter
csvline += directions_result[0]['copyrights']
print(csvline)