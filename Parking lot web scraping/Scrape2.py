import urllib.request
from bs4 import BeautifulSoup
import time
from pathlib import Path
import csv

uri = ''
html = urllib.request.urlopen(uri).read()
soup = BeautifulSoup(html, features="html.parser")
# Es gibt nur eine Tabelle
table = soup.select("table")[0]
currentTimestamp = time.strftime("%Y-%m-%d %X")
csv_rows = []
for row in table.findAll('tr')[1:]:
	csv_cells = [currentTimestamp]
	for cell in row.findAll('td')[:2]:
		text = cell.text
		if text.find("XXXX") != -1:
			text = "XXXXX"
		csv_cells.append(text.strip())
	csv_rows.append(csv_cells)

file_name = 'parksituation.csv'
path = str(Path(__file__).parent)

with open(path + '\\' + file_name, "a", newline='\n') as file:
	csvWriter = csv.writer(file)
	for data in csv_rows:
		csvWriter.writerow(data)
