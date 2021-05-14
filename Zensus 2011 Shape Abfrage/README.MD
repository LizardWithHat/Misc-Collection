This script will take a list of polygons exported as GeoJSON from qGIS as input. The script then queries the Zensus Atlas 2011 to extract the exact amount of inhibitants in the corresponding polygons. The result will be written back as a GeoJSON with the number of inhabitants injected as an property.
The point of the script is to get an exact amount of inhibitants, since the website only provides inexact values upon use.

The script uses the pip package EasyGUI to display an easy to use file picker for both input and output.