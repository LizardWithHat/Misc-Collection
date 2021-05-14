import subprocess
import os
import re
import time
from tabulate import tabulate
from flask import Flask, escape, request, render_template, Response

def trimWhitespaces(line):
	return re.sub(' +', ' ', line)
	
def queryPC(computername):
	environ = os.environ.copy()
	environ['PYTHONIOENCODING'] = 'ansi'
	resultString = ""
	computerString = '<h3 class="col-sm-8">Computer: ' + computername + '</h3>'
	buttonString = '<button  class="rdpbutton btn btn-outline-primary col-sm" type="button" id="rdp_' + computername + '">Connect</button>'
	header = '<div class="container alert ALERTTYPE" role="alert"><div class="row">'+ computerString + buttonString +'</div><br>'
	args = ["query", "user", "/server:"+computername]
	print("Querying %s" % computername)
	childProcess = subprocess.Popen(args, capture_output=True)
	try:
		out, errs = childProcess.communicate(timeout=1)
		out += errs
		resultString += trimWhitespaces(out.replace("rdp-tcp", "Remote").replace("console","Physisch").replace("\x81","ü"))
	except subprocess.TimeoutExpired:
		print("Killing Process for %s" % computername)
		resultString = "Error - Computer did not answer"
	
	if (resultString.find("Error") != -1):
		#Computer not available
		resultString = header.replace("ALERTTYPE", "alert-danger")+'The computer was not available.</div>'
		resultString = resultString.replace('type="button"', 'type="button" disabled')
		
	elif (resultString.find("*") != -1):
		#no users logged in
		resultString = header.replace("ALERTTYPE","alert-success")+'No users logged in at the current time.</div>'
		
	else:
		#at least one user logged in
		tableRows = resultString.split("\n")
		tableRows[0] += " TIME"
		tableHeaders = tableRows.pop(0).split(" ")
		table = []
		for row in tableRows:
			table.append(row.split(" ")[1:])
		
		resultString = header.replace("ALERTTYPE", "alert-warning")+tabulate(table[:-1], tableHeaders[1:], tablefmt="html") + '</div>'
		resultString = resultString.replace("\n","").replace("table", 'table class="table table-responsive"')
	return resultString

app = Flask(__name__)
@app.route('/available_ws_admin', methods=['GET'])
def available_ws_admin():
	try:
		formResult = request.args.get("computer")
		if not formResult:
			raise KeyError
		computers = formResult.replace(" ","").split(",")
	except KeyError:
		computers = []

	if len(computers) == 0:
		computers = ["Computer1, Computer2, Computer3"]

	results = []
	for computer in computers:
		results.append(queryPC(computer))
		
	resultText = str(results)[2:-2].replace("'", "").replace(",","").replace("<br>","")
	return render_template('availablility_overview_admin.html', text=resultText)
	

@app.route('/available_ws')
def available_ws():
	#Static computernames and their installed software
	computers = {
	"Computer01":[
	"Software A"
	], 
	
	"Computer02":[
	"Software A"
	],
	
	"Computer03":[
	"Software A",
	"Software B",
	"Software C"
	],
	}
	
	results = []
	for computer in computers.keys():
		availableSoftwareString = "Available software: "
		availableSoftwareString += '<ul class="list-group list-group-horizontal">'
		for software in computers.get(computer):
			availableSoftwareString += '<li class="list-group-item">'+software+'</li>'
		availableSoftwareString += '</ul>'
		
		results.append(queryPC(computer).replace("<br>", availableSoftwareString))
		
	resultText = str(results)[2:-2].replace("'", "").replace(",","")
	return render_template('availablility_overview_customer.html', text=resultText)