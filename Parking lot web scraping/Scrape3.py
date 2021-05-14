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
table_rows = []
for row in table.findAll('tr'):
	row_cells = [currentTimestamp]
	for cell in row.findAll('td'):
		text = cell.text
		row_cells.append(text.strip())
	table_rows.append(row_cells)

file_name = 'parksituation.csv'
path = str(Path(__file__).parent)

with open(path + '\\' + file_name, "a", newline='\n') as file:
	csvWriter = csv.writer(file)
	for data in table_rows[1:]:
		csvWriter.writerow(data)
