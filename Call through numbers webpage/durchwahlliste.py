import subprocess
import os
import re
import csv
from tabulate import tabulate
from flask import Flask, escape, request, render_template, Response

app = Flask(__name__)

@app.route('/durchwahlliste')
def durchwahlliste():
	durchwahlArray = []
	with open('durchwahlliste.csv', 'r') as csvFile:
		csvReader = csv.reader(csvFile, delimiter=";")
		for row in csvReader:
			durchwahlArray.append(row)
	headers = ["Vorname","Nachname","Kürzel","Durchwahl", "Home Office Nummer"]
	htmlText = tabulate(durchwahlArray, headers, tablefmt="html").replace("<table>", "<table class=\"table-bordered table-striped thead-light table-hover table-sm>\"").strip()
			
	return render_template('durchwahlliste.html', text=htmlText)