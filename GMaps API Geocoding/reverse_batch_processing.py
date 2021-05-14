import threading
import time
import googlemaps
import argparse
import json
import csv
import easygui
import chardet

class Geocoder(threading.Thread):
	lock = threading.Lock()	
	csvFile = "Input;Address;\n"
		
	def get_address_from_geocode(coordinates, o="NONE"):
		if not coordinates:
			pass
	
		api_key = "XXXXXXXXXXXXXXXXXXXXXXXXX"
		gmaps = googlemaps.Client(key=api_key)
		geocode_result = gmaps.reverse_geocode(coordinates[0])
	
		#Write output to given file
		if not (o == "NONE"):
			raw_json = json.dumps(geocode_result, sort_keys=True, indent=4)
			with open(o, "w") as file:
				file.write(raw_json)

		#Assemble CSV Line and output
		#Expected CSV Header: Input, Address
		delimiter = ";"
		csvline = ""
		if(geocode_result):
			csvline += str(coordinates) + delimiter
			csvline += geocode_result[0]['formatted_address'] + delimiter
		else:
			csvline += "ERROR: Couldn't find " + str(coordinates) + delimiter
			csvline += str(0) + delimiter
	
		return csvline
	
	def __init__(self, coordinates, o="NONE"):
		self.coordinates = coordinates
		self.o = o
		threading.Thread.__init__(self)
	
	def run(self):
		resolved_coordinates = Geocoder.get_address_from_geocode(self.coordinates, self.o)
		type(self).lock.acquire()
		type(self).csvFile += resolved_coordinates+"\n"
		type(self).lock.release()

#Use EasyGUI for File Choosing Dialog Boxes
source_file = easygui.fileopenbox("Quelldatei auswählen")
destination_file = easygui.filesavebox("Zieldatei auswählen", default="target.csv", filetypes='\*.csv')

#Use Chardet to determine CSV File Encoding
csv_encoding = ""
with open(source_file, 'rb') as source_csv_file:
	csv_encoding = chardet.detect(source_csv_file.read())['encoding']

address_stack = []
with open(source_file, 'r', encoding=csv_encoding) as source_csv_file:
	reader = csv.reader(source_csv_file, delimiter=';')
	for row in reader:
		address_stack.append(row)

#Batch workers in groups of 50, as 50 replies are the secondly quota
while len(coordinates_stack) > 0:
	try:
		if len(coordinates_stack) > 50:
			max_threads = 50
		else: 
			max_threads = len(coordinates_stack)
		threads = []
		for x in range(0, max_threads):
			t = Geocoder(coordinates_stack.pop())
			t.start()
			threads += [t]	
		#Wait for Thread Completion and guarantee one second of sleep to not hit quota limit
		for thread in threads:
			thread.join()
		time.sleep(1)
	except:
		print("Error: unable to start Threads" + sys.exc_info()[0])
		
with open(destination_file, 'w', newline='', encoding='utf-8') as destination_csv_file:
	destination_csv_file.write(Geocoder.csvFile)