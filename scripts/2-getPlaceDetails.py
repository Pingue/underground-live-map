#!/usr/bin/python
import urllib2
import json

print

response = urllib2.urlopen('https://api.tfl.gov.uk/Place?lat=51.5465906&lon=-0.4761759&radius=200&&app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
html=response.read()
parsed=json.loads(html)

bus=set()
tube=set()
print "Nearby Places:"
for i in parsed["places"]:

	if i["placeType"]=="StopPoint":
		if i["stopType"]=="NaptanMetroStation":
			print i["commonName"]
#			print "TUBE"
		elif i["stopType"]=="NaptanOnstreetBusCoachStopPair":
			print i["commonName"]
#			print "BUS"
		else:
			print i["stopType"]
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
		print i["commonName"]
#		print "OYSTER SHOP"
print 
print "Nearby Lines:"
print "buses: " 
for b in bus:
	print b

print

print "tubes: "
for t in tube:
	print t
#print json.dumps(parsed["places"],indent=5,sort_keys=True)
#print json.dumps(parsed,indent=4,sort_keys=True)
