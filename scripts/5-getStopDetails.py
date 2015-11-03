#!/usr/bin/python
import urllib2
import json
import cgi
import numpy
import dateutil.parser
import datetime

# Declare Variables ##########################################################################################

lines=""
stops=set()
arguments = cgi.FieldStorage()
facilities=dict()
accessibility=dict()
address=dict()
direction=dict()
geo=dict()
icons=""
table=""
addressLine=""
latlong=""
tubelink=""
buslink=""
arrivals=set()
departureTable=""
busDepartureTable=""

# Grab data and parse ########################################################################################

if "id" in arguments:
	id = arguments["id"].value
else:
	id="940GZZLUUXB"

response = urllib2.urlopen('https://api.tfl.gov.uk/StopPoint/'+id+'?app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
html=response.read()
parsed=json.loads(html)

response = urllib2.urlopen('https://api.tfl.gov.uk/StopPoint/'+id+'/Arrivals?app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
html=response.read()
parseddepartures=json.loads(html)

# If I am a stop cluster
if ("stopType" in parsed) and (parsed["stopType"] == "NaptanOnstreetBusCoachStopCluster"):
	for j in parsed["children"]:
		stops.add(j["id"])

# If my children are stop clusters
for i in parsed["children"]:
	if (i["placeType"]=="StopPoint") and ("stopType" in i) and (i["stopType"]=="NaptanOnstreetBusCoachStopCluster"):
		for j in i["children"]:
			stops.add(j["id"])

# Get the buses for each stop in the cluster
for stop in stops:
	response = urllib2.urlopen('https://api.tfl.gov.uk/StopPoint/'+stop+'/Arrivals?app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
	html=response.read()
	parsedbusdepartures=json.loads(html)
	for i in parsedbusdepartures:
		eta = dateutil.parser.parse(i["expectedArrival"]).strftime("%H:%M:%S")
		howlong = str(datetime.timedelta(seconds=i["timeToStation"]))
		busDepartureTable += "<tr><td>"+i["lineName"]+"</td><td>"+i["platformName"]+"</td><td>"+eta+" ("+howlong+")</td></tr>"

	

# Print Debug Output #########################################################################################

if ("debug" in arguments):
	print
	if (arguments["debug"].value=="2"):
		print json.dumps(parsed,indent=5,sort_keys=True)
		print

# Convert parsed to arrays ################################################################################

for i in parsed["additionalProperties"]:
	if i["category"]=="Direction":
		direction[i['key']] = i['value']
	if i["category"]=="Address":
		address[i['key']] = i['value']
	if i["category"]=="Accessibility":
		accessibility[i['key']] = i['value']
	if i["category"]=="Geo":
		geo[i['key']] = i['value']
	if i["category"]=="Facility":
		facilities[i['key']] = i['value']

# Convert arrays to strings ##################################################################################

# Lat/Long
latlong=str(parsed["lat"]) + "," + str(parsed["lon"])

# Departure List (Parent)
for i in parseddepartures:
	eta = dateutil.parser.parse(i["expectedArrival"]).strftime("%H:%M:%S")
	howlong = str(datetime.timedelta(seconds=i["timeToStation"]))
	departureTable += "<tr><td>"+i["lineName"]+"</td><td>"+i["platformName"]+"</td><td>"+eta+" ("+howlong+")</td></tr>"

# Address
if "Address" in address:
	addressLine+=address["Address"]
if "Postcode" in address:
	addressLine+=", " + address["postcode"]

# Facilities (& icons)
if "Bridge" in facilities:
	table += "<tr><td>Bridge</td><td>" + facilities["Bridge"] + "</td></tr>"
if "Escalators" in facilities:
	table += "<tr><td>Escalators</td><td>" + facilities["Escalators"] + "</td></tr>"
	if facilities["Escalators"] == "yes":
		icons += "<img src='/data/icons/glyphicons/glyphicons-420-disk-export.png'></img>"
if "Payphones" in facilities:
	table += "<tr><td>Payphones</td><td>" + facilities["Payphones"] + "</td></tr>"
	if facilities["Payphones"] != "0":
		icons += "<img src='/data/icons/glyphicons/glyphicons-442-phone-alt.png'></img>"
if "Boarding Ramps" in facilities:
	table += "<tr><td>Boarding Ramps</td><td>" + facilities["Boarding Ramps"] + "</td></tr>"
	if facilities["Boarding Ramps"] != "no":
		icons += "<img src='/data/icons/glyphicons/glyphicons-98-vector-path-line.png'></img>"
if "WiFi" in facilities:
	table += "<tr><td>Wifi</td><td>" + facilities["WiFi"] + "</td></tr>"
	if facilities["WiFi"] != "no":
		icons += "<img src='/data/icons/glyphicons/glyphicons-74-wifi.png'></img>"
if "Waiting Room" in facilities:
	table += "<tr><td>Waiting Room</td><td>" + facilities["Waiting Room"] + "</td></tr>"
	if facilities["Waiting Room"] == "yes":
		icons += "<img src='/data/icons/glyphicons/glyphicons-55-clock.png'></img>"
if "Photo Booths" in facilities:
	table += "<tr><td>Photo Booths</td><td>" + facilities["Photo Booths"] + "</td></tr>"
	if facilities["Photo Booths"] != "0":
		icons += "<img src='/data/icons/glyphicons/glyphicons-12-camera.png'></img>"
if "Lifts" in facilities:
	table += "<tr><td>Lifts</td><td>" + facilities["Lifts"] + "</td></tr>"
	if facilities["Lifts"] != "0":
		icons += "<img src='/data/icons/glyphicons/glyphicons-214-up-arrow.png'></img>"
if "Car park" in facilities:
	table += "<tr><td>Car Park</td><td>" + facilities["Car park"] + "</td></tr>"
	if facilities["Car park"] == "yes":
		icons += "<img src='/data/icons/glyphicons/glyphicons-6-car.png'></img>"
if "Toilets" in facilities:
	table += "<tr><td>Toilets</td><td>" + facilities["Toilets"] + "</td></tr>"
	if facilities["Toilets"] != "no":
		icons += "<img width=32 height=32  src='/data/icons/toilets.png'></img>"
if "Ticket Halls" in facilities:
	table += "<tr><td>Ticket Halls</td><td>" + facilities["Ticket Halls"] + "</td></tr>"
	if facilities["Ticket Halls"] != "0":
		icons += "<img src='/data/icons/glyphicons/glyphicons-287-fabric.png'></img>"
if "Euro Cash Machines" in facilities:
	table += "<tr><td>Euro Cash Machines</td><td>" + facilities["Euro Cash Machines"] + "</td></tr>"
	if facilities["Euro Cash Machines"] == "yes":
		icons += "<img src='/data/icons/glyphicons/glyphicons-227-euro.png'></img>"
if "Cash Machines" in facilities:
	table += "<tr><td>Cash Machines</td><td>" + facilities["Cash Machines"] + "</td></tr>"
	if facilities["Cash Machines"] != "0":
		icons += "<img src='/data/icons/glyphicons/glyphicons-459-money.png'></img>"
if "Help Points" in facilities:
	table += "<tr><td>Help Points</td><td>" + facilities["Help Points"] + "</td></tr>"
	helppoints = [int(s) for s in facilities["Help Points"].split() if s.isdigit()]
	nonzero=str(len(numpy.nonzero(helppoints)[0]))
	if nonzero != "0": 
		icons += "<img src='/data/icons/glyphicons/glyphicons-195-circle-question-mark.png'></img>"
if "Gates" in facilities:
	table += "<tr><td>Gates</td><td>" + facilities["Gates"] + "</td></tr>"
if "Other Facilities" in facilities:
	table += "<tr><td>Other Facilities</td><td>" + facilities["Other Facilities"] + "</td></tr>"

# List of lines
for i in parsed["lineModeGroups"]:
	for k in i["lineIdentifier"]:
		if i["modeName"] == "bus":
			buslink += "<a class= 'btn btn-small btn-default btn-danger' href='/data/scripts/6-lineAndStop.py?line="+k+"&stop="+id+"'>"+k+"</a>"
		elif i["modeName"] == "tube":
			tubelink += "<a class='btn btn-small btn-default btn-primary' href='/data/scripts/6-lineAndStop.py?line="+k+"&stop="+id+"'>"+k+"</a>"

if len(buslink) > 0:
	lines += "<tr><td>Bus lines</td><td><div class='btn-group' role='group'>" + buslink + "</div></td></tr>"
if len(tubelink) > 0:
	lines += "<tr><td>Tube lines</td><td><div class='btn-group' role='group'>" + tubelink + "</div></td></tr>"

# Print Header ###############################################################################################

print "Content-Type: text/html"
print

# Print the page #############################################################################################

print "<head>"
print '<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>'
print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js" integrity="sha256-Sk3nkD6mLTMOF0EOpNtsIry+s1CsaqQC1rVLTAy+0yc= sha512-K1qjQ+NcF2TYO/eI3M6v8EiNYZfA95pQumfvcVrTHtwQVDG+aHRqLi/ETn2uB+1JqwYqVG3LIvdm9lj6imS/pQ==" crossorigin="anonymous"></script>'
print '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet" integrity="sha256-MfvZlkHCEqatNoGiOXveE8FIwMzZg4W85qfrfIFBfYc= sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">'
print "</head><body>"
print '<nav class="navbar navbar-default navbar-inverse">\
  <div class="container-fluid">\
    <!-- Brand and toggle get grouped for better mobile display -->\
    <div class="navbar-header">\
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">\
        <span class="sr-only">Toggle navigation</span>\
        <span class="icon-bar"></span>\
        <span class="icon-bar"></span>\
        <span class="icon-bar"></span>\
      </button>\
      <a class="navbar-brand" href="#">Transporter</a>\
    </div>\
\
    <!-- Collect the nav links, forms, and other content for toggling -->\
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">\
      <ul class="nav navbar-nav">\
        <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li>\
        <li><a href="#">Link</a></li>\
        <li class="dropdown">\
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>\
          <ul class="dropdown-menu">\
            <li><a href="#">Action</a></li>\
            <li><a href="#">Another action</a></li>\
            <li><a href="#">Something else here</a></li>\
            <li role="separator" class="divider"></li>\
            <li><a href="#">Separated link</a></li>\
            <li role="separator" class="divider"></li>\
            <li><a href="#">One more separated link</a></li>\
          </ul>\
        </li>\
      </ul>\
      <form class="navbar-form navbar-left" role="search">\
        <div class="form-group">\
          <input type="text" class="form-control" placeholder="Search">\
        </div>\
        <button type="submit" class="btn btn-default">Submit</button>\
      </form>\
      <ul class="nav navbar-nav navbar-right">\
        <li class="dropdown">\
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Drop <span class="caret"></span></a>\
          <ul class="dropdown-menu">\
            <li><a href="#">Action</a></li>\
            <li><a href="#">Another action</a></li>\
            <li><a href="#">Something else here</a></li>\
            <li role="separator" class="divider"></li>\
            <li><a href="#">Separated link</a></li>\
          </ul>\
        </li>\
      </ul>\
    </div><!-- /.navbar-collapse -->\
  </div><!-- /.container-fluid -->\
</nav>'
print "<h1>" + parsed["commonName"] +"  <small><span class='text-nowrap'>" + addressLine + "</span></small></h1>"
print "Lat/Long: " + latlong + " "
print "<a href='https://www.google.co.uk/maps/@"+latlong+",17z'>Google Maps</a>, "
print "<a href='https://www.google.co.uk/maps/@"+latlong+",700m/data=!3m1!1e3'>Google Satellite</a>, "
print "<a href='https://www.ingress.com/intel?ll="+latlong+"&z=17'>Ingress Intel</a> "

print "<table>"
print lines
print "</table>"

print icons
print "<p>"
if busDepartureTable != "":
	print "<table class='table table-striped table-hover table-bordered table-condensed'>"
	print "<thead><th>Line</th><th>Stop</th><th>ETA</th></thead><tbody>"
	print busDepartureTable
	print "</table>"
if departureTable != "":
	print "<table class='table table-striped table-hover table-bordered table-condensed'>"
	print "<thead><th>Line</th><th>Platform</th><th>ETA</th></thead><tbody>"
	print departureTable
	print "</table>"
if table != "":
	print "<table class='table table-striped table-hover table-bordered table-condensed'>"
	print "<thead><th>Facilities</th><th></th></thead>"
	print table
	print "</table>"
