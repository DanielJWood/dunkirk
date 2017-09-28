import time
import copy
import csv
import simplejson as json

def rounders(d,r):
	if (d == "NA"):
		return "null"
	else:
		return round(float(d), r) 

def floater(d):
	if (d == "NA"):
		return "null"
	else:
		return float(d) 		

# load the overarching csv
with open('cardTest.csv', 'rb') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Load the templates
with open('pre.json') as pre_data:
    pre = json.load(pre_data)

output = copy.deepcopy(pre)
index = {}

# timeNow = time.strftime("%H:%M:%S")
# print timeNow
# output["metadata"]["name"] = "Dunkirk @ " + timeNow
# # print groupTemplate
# # print tempGroupTemplate
# # tempGroupTemplate["lead"] = "Group Lead Test"
# # print groupTemplate
# # print tempGroupTemplate
# print groupTemplate
# tempGroupTemplate = groupTemplate.copy()

for i in range(1, len(rows)):
	cardNum = rows[i][0]
	if cardNum not in index:
		index[cardNum] = {}			
		# declare the variables for the group

		with open('groupTemplate.json') as groupTemplate_data:
		    groupTemplate = json.load(groupTemplate_data)    

		groupTemplate["metadata"]["name"] = rows[i][6]
		groupTemplate["title"] = "Group title Test"
		groupTemplate["lead"] = "Group Lead Test"
		groupTemplate["text"] = rows[i][10]
		groupTemplate["id"] = cardNum

		# Make the group
		output["groups"].append(groupTemplate)
		# print output

# for every group, create polygons inside that group/card if they have the correct ID
for j in range(0, len(output["groups"])):
	for i in range(1,len(rows)):	
		if rows[i][0] == output["groups"][j]["id"]:
		
			url = "editedshps/finished/json/" + rows[i][1]
			# Open GeoJSON from the csv row
			with open(url) as json_data:
			    d = json.load(json_data)

			# for each item of MultiPolygon, create a polygon in eartheos

			if d["features"][0]["geometry"]["type"] == "MultiPolygon":
				for k in range(0, len(d["features"][0]["geometry"]["coordinates"])):

					with open('polygonTemplate.json') as polygonTemplate_data:
						polygonTemplate = json.load(polygonTemplate_data)

					polygonTemplate["title"] = rows[i][3]
					polygonTemplate["lead"] = rows[i][4]
					polygonTemplate["text"] = rows[i][5]					
					polygonTemplate["style"]["color"] = rows[i][2]
					polygonTemplate["camera"]["lat"] = float(rows[i][7])
					polygonTemplate["camera"]["lon"] = float(rows[i][8])
					polygonTemplate["camera"]["height"] = float(rows[i][9])
					polygonTemplate["camera"]["duration"] = float(rows[i][12])

					bounds = []

					for x in range(0,len((d["features"][0]["geometry"]["coordinates"][k][0]))):
						longitude = d["features"][0]["geometry"]["coordinates"][k][0][x][0]
						latitude = d["features"][0]["geometry"]["coordinates"][k][0][x][1]
						bounds.append([latitude,longitude])

					polygonTemplate["bounds"] = bounds

					# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]
					if output["groups"][j]["id"] == "0":						
						output["layers"][0]["polygons"].append(polygonTemplate)
					else: 
						output["groups"][j]["layers"][0]["polygons"].append(polygonTemplate)
			elif d["features"][0]["geometry"]["type"] == "Polygon":
				with open('polygonTemplate.json') as polygonTemplate_data:
					polygonTemplate = json.load(polygonTemplate_data)

				polygonTemplate["title"] = rows[i][3]
				polygonTemplate["lead"] = rows[i][4]
				polygonTemplate["text"] = rows[i][5]
				polygonTemplate["style"]["color"] = rows[i][2]
				polygonTemplate["camera"]["lat"] = float(rows[i][7])
				polygonTemplate["camera"]["lon"] = float(rows[i][8])
				polygonTemplate["camera"]["height"] = float(rows[i][9])

				bounds = []

				for x in range(0,len((d["features"][0]["geometry"]["coordinates"][0]))):
					longitude = d["features"][0]["geometry"]["coordinates"][0][x][0]
					latitude = d["features"][0]["geometry"]["coordinates"][0][x][1]
					bounds.append([latitude,longitude])

				polygonTemplate["bounds"] = bounds

				# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]

				output["groups"][j]["layers"][0]["polygons"].append(polygonTemplate)
			else:	
				print "error in coords and polygon type"

output["groups"][0]["layers"][0]["polygons"][0]["audioURL"] = "https://github.com/DanielJWood/dunkirk/blob/master/guns.mp3?raw=true"
# output["layers"][0]["polygons"][0]["audioURL"] = "https://github.com/DanielJWood/dunkirk/blob/master/guns.mp3?raw=true"
# output["layers"][0]["polygons"][0]["title"] = "Prewar boundaries"

# print output["layers"][0]["polygons"][0]["audioURL"]

# print May10["features"][0]["geometry"]["type"]
# print len(May10["features"][0]["geometry"]["coordinates"]) #Number of polygons
# print len(May10["features"][0]["geometry"]["coordinates"][i]) #Index at polygon
# print len(May10["features"][0]["geometry"]["coordinates"][i][0]) #number of coord-pairs on that polygon
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j]) #Pair of coordinates
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j][0]) #Longitude
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j][1]) #latitude

# print output

with open('dunkirk.json', 'w') as f:
    json.dump(output, f)    

