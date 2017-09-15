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
# print output
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

for j in range(0, len(output["groups"])):
	for i in range(1,len(rows)):	
		if rows[i][0] == output["groups"][j]["id"]:
		
			with open('polygonTemplate.json') as polygonTemplate_data:
				polygonTemplate = json.load(polygonTemplate_data)

			polygonTemplate["title"] = rows[i][3]
			polygonTemplate["lead"] = rows[i][4]
			polygonTemplate["text"] = rows[i][5]
			polygonTemplate["style"]["color"] = rows[i][2]
			polygonTemplate["camera"]["lat"] = float(rows[i][7])
			polygonTemplate["camera"]["lon"] = float(rows[i][8])
			polygonTemplate["camera"]["height"] = float(rows[i][9])

			with open(rows[i][1]) as json_data:
			    d = json.load(json_data)

			bounds = []

			for i in range(0,len((d["features"][0]["geometry"]["coordinates"][0]))):
				longitude = d["features"][0]["geometry"]["coordinates"][0][i][0]
				latitude = d["features"][0]["geometry"]["coordinates"][0][i][1]
				bounds.append([latitude,longitude])

			polygonTemplate["bounds"] = bounds

			# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]

			output["groups"][j]["layers"][0]["polygons"].append(polygonTemplate)



# with open('simple.geoJSON') as json_data:
#     d = json.load(json_data)

# with open('simple2.geoJSON') as json_data2:
#     d2 = json.load(json_data2)    



# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]
# print pre["groups"][0]["layers"][0]["polygons"][1]["bounds"]


# for each date
	# for each geo file in date
		# for each polygon item of json
			# if multipolygon
				# for each in multipolygon
					# reverse lat long, add in metadata
			# if not multipolgyon
				# reverse lat long, add in meta data



# for i in range(0,len((d["features"][0]["geometry"]["coordinates"][0]))):
# 	longitude = d["features"][0]["geometry"]["coordinates"][0][i][0]
# 	latitude = d["features"][0]["geometry"]["coordinates"][0][i][1]
# 	output1.append([latitude,longitude])

# for i in range(0,len((d2["features"][0]["geometry"]["coordinates"][0]))):
# 	longitude = d2["features"][0]["geometry"]["coordinates"][0][i][0]
# 	latitude = d2["features"][0]["geometry"]["coordinates"][0][i][1]
# 	output2.append([latitude,longitude])	

# pre["groups"][0]["layers"][0]["polygons"][0]["bounds"] = output1	
# pre["groups"][0]["layers"][0]["polygons"][1]["bounds"] = output2
	
# print output

with open('simpleout.json', 'w') as f:
    json.dump(output, f)    

