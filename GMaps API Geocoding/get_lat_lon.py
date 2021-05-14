import googlemaps
import argparse
import json

def get_geocode_from_address(address, o="NONE"):
	if not address:
		pass
	
	api_key = "XXXXXXXXXXXXXXXXXX"
	gmaps = googlemaps.Client(key=api_key)
	geocode_result = gmaps.geocode(args.address)
	
	#Write output to given file
	if not (o == "NONE"):
		raw_json = json.dumps(geocode_result, sort_keys=True, indent=4)
		with open(o, "w") as file:
			file.write(raw_json)

	#Assemble CSV Line and output
	#Expected CSV Header: Address, Latitude, Longitude
	delimiter = ";"
	csvline = ""
	if(geocode_result):
		csvline += geocode_result[0]['formatted_address'] + delimiter
		csvline += str(geocode_result[0]['geometry']['location']['lat']) + delimiter
		csvline += str(geocode_result[0]['geometry']['location']['lng']) + delimiter
	else:
		csvline += "ERROR: Couldn't find "+args.address + delimiter
		csvline += str(0) + delimiter
		csvline += str(0) + delimiter
	
	return csvline

if __name__ == '__main__:
	#neccessary argument
	argparser = argparse.ArgumentParser()
	argparser.add_argument("address", help="Address that you want to process")
	#optional argument
	argparser.add_argument("-o", "--outputfile", help="where to parse the received raw data")
	args = argparser.parse_args()

	csvline = get_geocode_from_address(args.address, o=args.outputfile)

	print(csvline)