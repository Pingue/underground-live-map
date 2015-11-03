#!/usr/bin/python
import urllib2
import json
import cgi
print "Content-Type: text/html"
print

arguments = cgi.FieldStorage()
lat = "51.5465906"
lon = "-0.4761760"
radius = "200"
if "lat" in arguments:
	lat=arguments["lat"].value
if "lon" in arguments:
	lon=arguments["lon"].value
if "radius" in arguments:
	radius=arguments["radius"].value

response = urllib2.urlopen('https://api.tfl.gov.uk/Place?lat='+lat+'&lon='+lon+'&radius='+radius+'&app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
html=response.read()
parsed=json.loads(html)

bus=set()
tube=set()
print "Nearby Places:<br/>"
for i in parsed["places"]:

	if i["placeType"]=="StopPoint":
		if i["stopType"]=="NaptanMetroStation":
			print "<a href='5-getStopDetails.py?id=" + i["id"] + "'>" + i["commonName"] + "</a><br/>"
#			print "TUBE"
		elif i["stopType"]=="NaptanOnstreetBusCoachStopCluster":
			print "<a href='5-getStopDetails.py?id=" + i["id"] + "'>" + i["commonName"] + "</a><br/>"
#			print "BUS"
		elif i["stopType"]=="NaptanOnstreetBusCoachStopPair":
			print "<a href='5-getStopDetails.py?id=" + i["id"] + "'>" + i["commonName"] + "</a><br/>"
#			print "BUS"
		else:
			print "UNKNOWN TRANSPORT TYPE: " + i["stopType"] + ", " + i["commonName"] + ", " + i["id"] +"<br/>"

#		print "GETTING LINES"
		for j in i["lineModeGroups"]:
#			print j["lineIdentifier"]
			for k in j["lineIdentifier"]:
				if j["modeName"] == "bus":
					bus.add(k)			
				elif j["modeName"] == "tube":
					tube.add(k)			
	elif i["placeType"]=="CensusOutputAreas":
		continue	
#		print "CENSUS OUTPUT AREA. IGNORING"
	elif i["placeType"]=="OysterTicketShop":
		print "<a href='2-getPlaceDetails.py?id=" + i["id"] + "'>" + i["commonName"] + "</a><br/>"
#		print "OYSTER SHOP"
print "<br/>" 
print "Nearby Lines:<br/>"
print "<a href='3-allLines.py?type=bus'>Buses:</a><br/>" 
for b in bus:
	print "<a href='4-line.py?line=" + b + "'>" + b + "</a><br/>"

print "<br/>"

print "<a href='3-allLines.py?type=tube'>Tubes:</a><br/>" 
for t in tube:
	print "<a href='4-line.py?line=" + t + "'>" + t + "</a><br/>"
#print json.dumps(parsed["places"],indent=5,sort_keys=True)
#print json.dumps(parsed,indent=4,sort_keys=True)
