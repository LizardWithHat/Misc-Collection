import urllib.request
from bs4 import BeautifulSoup
import time
from pathlib import Path
import csv

uri = ''
html = urllib.request.urlopen(uri).read()
soup = BeautifulSoup(html, features="html.parser")

# Elements of interest are not part of a list, they are however all elements of the class "elem"
table = soup.find(class_="parken-giessen").find_all(class_="elem")
currentTimestamp = time.strftime("%Y-%m-%d %X")
table_rows = []
for row in table:
	row_cells = [currentTimestamp]
	row_cells.append(row.find(class_="slot-name").text.strip())
	row_cells.append(row.find(class_="free").text.strip()[6:])
	row_cells.append(row.find(class_="max").text.strip()[8:])
	table_rows.append(row_cells)

file_name = 'parksituation.csv'
path = str(Path(__file__).parent)

with open(path + '\\' + file_name, "a", newline='\n') as file:
	csvWriter = csv.writer(file)
	for data in table_rows:
		csvWriter.writerow(data)
