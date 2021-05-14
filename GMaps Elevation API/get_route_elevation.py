import googlemaps
import json
import csv
import easygui

#Use EasyGUI for LAT,LONG,
user_input = easygui.multenterbox("Please fill out all fields",
"Google Route Elevation",
["Latitude Start","Longitude Start","Latitude Ende","Longitude Ende","Interval"],
["51.165691","10.451526","46.227638","2.213749","2"])
if user_input == None:
	exit()
latStart, longStart, latEnd, longEnd, samples = user_input
if int(samples) < 2:
	samples = "2"
api_key = "XXXXXXXXXXXXXXXXXXXXXXXX"
gmaps = googlemaps.Client(key=api_key)
elevation_result = gmaps.elevation_along_path([(float(latStart), float(longStart)),(float(latEnd), float(longEnd))], int(samples))

#Assemble CSV Line and output
#Expected CSV Header: Latitude, Longitude, Elevation in meters, Resolution in meters
delimiter = ";"
csvFile = "Latitude;Longitude;Elevation in meters;Resolution in meters\n"
if(elevation_result):
	for result in elevation_result:
		csvline = ""
		csvline += str(result['location']['lat']) + delimiter
		csvline += str(result['location']['lng']) + delimiter
		csvline += str(result['elevation']) + delimiter
		if	"resolution" in result.keys():
			csvline += str(result['resolution']) + delimiter
		else:
			csvline += "Unknown"
		csvline += "\n"
		
		csvFile += csvline
		
	#Use EasyGUI for File Choosing Dialog Boxes
	destination_file = easygui.filesavebox("Choose Target File", default="target.csv", filetypes='\*.csv')

	with open(destination_file, 'w', newline='', encoding='utf-8') as destination_csv_file:
		destination_csv_file.write(csvFile)
else:
	easygui.msgbox("Error: No results found.")