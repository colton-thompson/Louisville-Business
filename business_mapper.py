import sys
import csv
import pprint
import folium
import pandas

def reformatDate(df):
	newDateList = []
	for dateIndex in df["date"]:
		year = str(dateIndex)
		year = (year[0:4])

		month = str(dateIndex)
		month = month[5:6]
		
		day = str(dateIndex)
		day = day[7:8]
		
		newDate = year + "-" + month + "-" + day
		newDateList.append(newDate)
	return newDateList

#read in file, return dictionary
def creat_Dict_from_CSV(f):
	reader = csv.DictReader(open(f, 'r',))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list
	
def getPopupInfo(name, address):
	#score = attachScore()
	popup = name + "<br>Address: " + addy +"<br>Score: " + str(-1)
	return popup
	
def assign_Inspection_Score():
	dict_list = {}
	for bus_index in range(len(businessDict)):
		for insp_index in range(len(inspectionDict)):
			if (businessDict[bus_index]['business_id'] == inspectionDict[insp_index]['business_id']):
				print("match found at " + str(businessDict[bus_index]['business_id']) + "\tScore: " + inspectionDict[insp_index]['score'] + "\tDate: " + inspectionDict[insp_index]['date'] )
				
def filterDataFile_Businesses(df_b):
	df_b = df_b[df_b['latitude']!=0.0]
	df_b = df_b[df_b['longitude']!=0.0]
	#df_b = df_b[df_b.phone_number.notnull()]
	df_b = df_b.sort_values("business_id", ascending = True)
	#print(df_b.head(n=10))
	df_b = pandas.DataFrame({'business_id': df_b["business_id"],'name': df_b["name"],'address': df_b["address"], 'city':df_b["city"], 'state':df_b["state"], 'postal_code':df_b["postal_code"], 'latitude':df_b["latitude"],'longitude':df_b["longitude"], 'phone_number':df_b["phone_number"]}).to_csv('bus_test.csv')
	
def filterDataFile_Inspections(df_i):
	df_i = df_i[df_i['date'] > 20160000]
	df_i = df_i.dropna(subset = ['score']) #filter out scores of 0, nan, ect.
	df_i = df_i.sort_values("date", ascending = False)
	#print(df_i.head(n=1000))
	df_i = pandas.DataFrame({'business_id': df_i["business_id"],'score': df_i["score"],'date': df_i["date"], 'description':df_i["description"], 'type':df_i["type"]}).to_csv('insp_test.csv')
				
				
# check if files are up to date otherwise update them
# run this section first and save the filtered data as a new csv
# read files
df_b = pandas.read_csv("businesses.csv")#, nrows = 10)
df_i = pandas.read_csv("inspections.csv")

#filter data
filterDataFile_Businesses(df_b)
#df_i["date"] = reformatDate(df_i)
filterDataFile_Inspections(df_i)

#create dictionaries

businessDict = creat_Dict_from_CSV("bus_test.csv")
inspectionDict = creat_Dict_from_CSV("insp_test.csv")

mergedDict = assign_Inspection_Score()

print(businessDict[0]['business_id'])
print(inspectionDict[0]['business_id'])


#Folium Mapping Section
map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start= 13)

fg = folium.FeatureGroup(name="Restuarants")
for la,lo,name,addy in zip(df_b["latitude"],df_b["longitude"],df_b["name"], df_b["address"]):
#for la,lo,name,addy in zip(businessDict["latitude"],businessDict["longitude"],businessDict["name"], businessDict["address"]):
	try:
		fg.add_child(folium.Marker(location=[la,lo], popup=(folium.Popup(getPopupInfo(name, addy),max_width=150,min_height=200)), icon=folium.Icon(color="red", icon_color='white')))
	except TypeError:
		raise
	
map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')