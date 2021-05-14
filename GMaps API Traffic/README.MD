This script takes a path definition via Command Line in a LAT:LONG format and gets traffic informations of that path from the Google Maps API. The raw results can be optionally exported. The csv formatted results will be printed out on the console and can be appended to a csv file via command line that way.

Example usage:

```"python.exe" "<PATH>\get_raw_directions.py" 51.514310,7.465280 51.437627,7.570480 -V 51.504208,7.517991 >> "FILE.csv"```