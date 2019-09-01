import sys
import csv
import pprint
import folium
import pandas
from datetime import date

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

def getDateFromOneYearAgo():
	today = date.today()
	d1 = today.strftime("%Y%m%d")
	d1 = int(d1) - 10000
	#print("d1 =", d1)
	return d1

#read in file, return dictionary
def creat_Dict_from_CSV(f):
	reader = csv.DictReader(open(f, 'r',))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list
	
def getPopupInfo(name, address, score):
	#score = attachScore()
	popup = name + "<br>Address: " + address +"<br>Health Inspection Score: " + str(score)
	return popup
	
def assign_Inspection_Score():
	dict_list = []
	for bus_index in range(len(businessDict)):
		for insp_index in range(len(inspectionDict)):
			bus_id = businessDict[bus_index]['business_id']
			ins_id = inspectionDict[insp_index]['business_id']
			if (bus_id == ins_id):
				#bus_id = businessDict[bus_index]['business_id']
				name = businessDict[bus_index]['name']
				address = businessDict[bus_index]['address']
				score = inspectionDict[insp_index]['score']
				lat = businessDict[bus_index]['latitude']
				lon = businessDict[bus_index]['longitude']
				dict_list.append({'business_id' : bus_id, 'name' : name, 'address' : address, 'score': score, 'latitude': lat, 'longitude': lon})
	return dict_list
				
def filterDataFile_Businesses(df_b):
	df_b = df_b[df_b['latitude']!=0.0]
	df_b = df_b[df_b['longitude']!=0.0]
	#df_b = df_b[df_b.phone_number.notnull()]
	df_b = df_b.sort_values("business_id", ascending = True)
	#print(df_b.head(n=10))
	df_b = pandas.DataFrame({'business_id': df_b["business_id"],'name': df_b["name"],'address': df_b["address"], 'city':df_b["city"], 'state':df_b["state"], 'postal_code':df_b["postal_code"], 'latitude':df_b["latitude"],'longitude':df_b["longitude"], 'phone_number':df_b["phone_number"]}).to_csv('bus_test.csv')
	
def filterDataFile_Inspections(df_i):
	compareDate = getDateFromOneYearAgo()
	df_i = df_i[df_i['date'] > compareDate]
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
#print(mergedDict)

#Folium Mapping Section
map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df_b['latitude'].mean(),df_b['longitude'].mean()],zoom_start= 13)

fg = folium.FeatureGroup(name="Restuarants")

for index in range(len(mergedDict)):
	#print(mergedDict[index])
	name = mergedDict[index]['name']
	lat = mergedDict[index]['latitude']
	lon = mergedDict[index]['longitude']
	address = mergedDict[index]['address']
	score = mergedDict[index]['score']
	fg.add_child(folium.Marker(location = [lat,lon], popup = folium.Popup(getPopupInfo(name, address, score), max_width=175,min_height=200), icon = folium.Icon(color = "red", icon_color = "white")))
	
map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')