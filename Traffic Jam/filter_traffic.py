from xml.dom.minidom import parse
import xml.dom.minidom
from pathlib import Path
from os import listdir

# Returns true if the point is withing the zone
# Format: zoneData: From Lat, From Long, To Lat, To Long
#					pInQuestion: Lat, Long
def isBetween(zoneData, pInQuestion):
	pFromLat, pFromLon, pToLat, pToLon = zoneData
	pInQuestionLat, pInQuestionLon = pInQuestion
	return ((pFromLat <= pInQuestionLat <= pToLat) or (pFromLat >= pInQuestionLat >= pToLat) and
					(pFromLon <= pInQuestionLon <= pToLon) or (pFromLon >= pInQuestionLon >= pToLon))

# Format: From Lat, From Long, To Lat, To Long
zone = [[51.286328, 6.269920, 51.21036, 6.379970],
[51.231543,  6.449191, 51.233592, 6.709558],
[51.237622,6.485908,  51.293900, 6.808391]]

file_out_name = "filteredTraffic.xml"

situationDict = {}

doc = xml.dom.minidom.Document()

docLogicalModel = doc.createElement("d2LogicalModel")
docLogicalModel.setAttribute("modelBaseVersion", "2")
docLogicalModel.setAttribute("xsi:schemaLocation", "http://datex2.eu/schema/2/2_0 http://bast.s3.amazonaws.com/schema/1442489426159/DATEXIISchema_2_2_0.xsd")
docLogicalModel.setAttribute("xmlns", "http://datex2.eu/schema/2/2_0")
docLogicalModel.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
docLogicalModel.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
doc.appendChild(docLogicalModel)

docRoot = doc.createElement('payloadPublication')
docRoot.setAttribute("xsi:type", "SituationPublication")
docRoot.setAttribute("lang", "de-DE")
docLogicalModel.appendChild(docRoot)

path = str(Path(__file__).parent)

for filename in listdir(path):
	if (not filename[-4:] == ".xml") or (filename == file_out_name):
		continue
	curXml = xml.dom.minidom.parse(path +"/" + filename)
	curTree = curXml.documentElement
	listOfSituations = curTree.getElementsByTagName("situation")
	for situation in listOfSituations:
		situationID = situation.getAttribute("id")
		if situationID in situationDict:
			# If the current version is older than the saved one, ignore
			if (situation.getElementsByTagName("situationVersionTime")[0].childNodes[0].data < situationDict[situationID].getElementsByTagName("situationVersionTime")[0].childNodes[0].data ):
				continue
			# If not, delete the entry
			else:
				del situationDict[situationID]

		pointTo = situation.getElementsByTagName("to")
		pointFrom = situation.getElementsByTagName("from")
		
		# There are situation-objects without "From" and "To" elements, like iced roads.
		# Those can be savely ignored for the purpose of this tool.
		if not pointTo:
			continue
		
		currFrom = [float(pointFrom[0].getElementsByTagName("latitude")[0].childNodes[0].data),	float(pointFrom[0].getElementsByTagName("longitude")[0].childNodes[0].data)]
		currTo = [float(pointTo[0].getElementsByTagName("latitude")[0].childNodes[0].data), float(pointTo[0].getElementsByTagName("longitude")[0].childNodes[0].data)]
		
		# Are the coordinates within the zones we want to check?
		if (isBetween(zone[0], currFrom) or isBetween(zone[0], currTo)
		or isBetween(zone[1], currFrom) or isBetween(zone[1], currTo)
		or isBetween(zone[2], currFrom) or isBetween(zone[2], currTo)
						
		# Do the coordinates wrap around a zone?
		or isBetween( currFrom + currTo, [ zone[0][0], zone[0][1] ])
		or isBetween( currFrom + currTo, [ zone[1][0], zone[1][1] ])
		or isBetween( currFrom + currTo, [ zone[2][0], zone[2][1] ])):
			situationDict[situationID] = situation
		
for situationID, situation in situationDict.items():
	docRoot.appendChild(situation)

# Write to a new document
file = open(path + "/" + file_out_name, "w", encoding='utf-8')
doc.writexml(file, encoding="UTF-8")
file.close()