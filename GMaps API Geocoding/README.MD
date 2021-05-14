This script uses the Google Maps API to geocode adresses to LAT:LONG coordinates (batch_processing) or vice versa(reverse_batch_processing). It takes a list of adresses or coordinates in a CSV format via a GUI and saves them back into a specified CSV file.
The CSV file is expected to just list the adress or coordinates, see the example included example csv file.

The script uses the additional pip modules googlemaps, cardet and easygui.