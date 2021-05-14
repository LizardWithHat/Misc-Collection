from xml.dom.minidom import parse
import xml.dom.minidom
from pathlib import Path
from os import listdir
import csv

# This script takes a XML-File in the DATEX II format and the name "filteredTraffic.xml" as input,
# and formats them to a CSV-File named "processedTrafficData.csv".
# The CSV has the following format:
# Start Time, Version Time, Comment, Latitude From, Longitude From, Latitude To, Longitude To, Status, Start Time, End time

file_in_name = "filteredTraffic.xml"
file_out_name = "processedTrafficData.csv"

path = str(Path(__file__).parent)
trafficXml = xml.dom.minidom.parse(path +"/" + file_in_name)
trafficTree = trafficXml.documentElement
listOfSituations = trafficTree.getElementsByTagName("situation")

with open('processedTraffic.csv', 'w', newline='\n') as file:		
	csvWriter = csv.writer(file, delimiter=';')
	headerRow = ["Start Time", "Version Time", "Comment", "Latitude From", "Longitude From", "Latitude To", "Longitude To", "Status", "Start Time", "End time"]
	csvWriter.writerow(headerRow)
	
	for situation in listOfSituations:
		pointTo = situation.getElementsByTagName("to")
		pointFrom = situation.getElementsByTagName("from")
		
		latFrom = pointFrom[0].getElementsByTagName("latitude")[0].childNodes[0].data
		longFrom = pointFrom[0].getElementsByTagName("longitude")[0].childNodes[0].data
		latTo = pointTo[0].getElementsByTagName("latitude")[0].childNodes[0].data
		longTo = pointTo[0].getElementsByTagName("longitude")[0].childNodes[0].data
		comment = situation.getElementsByTagName("comment")[0].getElementsByTagName("value")[0].childNodes[0].data.replace("\n", " ")
		status =  situation.getElementsByTagName("validityStatus")[0].childNodes[0].data
		recordCreationTime =  situation.getElementsByTagName("overallStartTime")[0].childNodes[0].data
		recordVersionTime =  situation.getElementsByTagName("situationVersionTime")[0].childNodes[0].data
		
		startTime = ""
		endTime = ""
		if status == 'definedByValidityTimeSpec':
			if situation.getElementsByTagName("startOfPeriod").length != 0:
				startTime = situation.getElementsByTagName("startOfPeriod")[0].childNodes[0].data
			endTime = situation.getElementsByTagName("endOfPeriod")[0].childNodes[0].data
		
		length = ""
		if situation.getElementsByTagName("lengthAffected").length != 0: 
			length =  situation.getElementsByTagName("lengthAffected")[0].childNodes[0].data
			
		situationRow = [recordCreationTime, recordVersionTime, comment, latFrom, longFrom, latTo, longTo, length, status, startTime, endTime]

		csvWriter.writerow(situationRow)