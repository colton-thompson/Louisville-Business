import sys
import csv
import pprint
import folium
import pandas
from datetime import date
from colorama import Fore, Back, Style 

def reformatDate(date):
	date = str(date)
	year = date[0:4]
	month = date[4:6]
	day = date[6:8]
	newDate = month + "/" + day + "/" + year 
	return newDate

def getDateFromOneYearAgo():
	today = date.today()
	d1 = today.strftime("%Y%m%d")
	d1 = int(d1) - 10000 #10000 is the X location in 201X0000
	return d1

#read in file, return dictionary
def creat_Dict_from_CSV(f):
	reader = csv.DictReader(open(f, 'r',))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list
	
def getScoreColor(score):
	if (float(score) >= 90):
		num = (Fore.GREEN + score)
	elif (float(score) >= 80):
		num = (Fore.BLUE + score)
	else:
		num = (Fore.RED + score)
	#print(Style.RESET_ALL)	
	print(num)
	return num
	
#TODO get colors to display correctly, currently return the numbers of the color and not the actual color8
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))	
	
def getPopupInfo(data):
	date = reformatDate(data['date'])
	score = data['score']
	#num = getScoreColor(score)
	popup =  data['name'] + "<br><b>Address: </b>" + data['address'] +"<br><b>Health Inspection Score: </b>" + score + " <br><b>Last Inspection: </b>" + date
	return popup
	
def color(score): 
	score = float(score)
	if score >= 90.0: 
		col = 'green'
	elif score >= 80.0: 
		col = 'blue'
	else:
		col='red'
	print(str(score) + " : " + col)
	return col 
	
def merge_dictionaries():
	dict_list = []
	for bus_index in range(len(businessDict)):
		for insp_index in range(len(inspectionDict)):
			bus_id = businessDict[bus_index]['business_id']
			ins_id = inspectionDict[insp_index]['business_id']
			if (bus_id == ins_id):
				name = businessDict[bus_index]['name']
				address = businessDict[bus_index]['address']
				score = inspectionDict[insp_index]['score']
				date = inspectionDict[insp_index]['date']
				lat = businessDict[bus_index]['latitude']
				lon = businessDict[bus_index]['longitude']
				
				dict_list.append({'business_id' : bus_id, 'name' : name, 'address' : address, 'score': score, 'date': date,'latitude': lat, 'longitude': lon})
	return dict_list
				
def filterDataFile_Businesses(df_b):
	df_b = df_b[df_b['latitude']!=0.0]
	df_b = df_b[df_b['longitude']!=0.0]
	#df_b = df_b[df_b.phone_number.notnull()]
	df_b = df_b.sort_values("business_id", ascending = True)
	#print(df_b.head(n=10))
	df_b = pandas.DataFrame({'business_id': df_b["business_id"],'name': df_b["name"],'address': df_b["address"], 'city':df_b["city"], 'state':df_b["state"], 'postal_code':df_b["postal_code"], 'latitude':df_b["latitude"],'longitude':df_b["longitude"], 'phone_number':df_b["phone_number"]}).to_csv('businesses copy.csv')
	
def filterDataFile_Inspections(df_i):
	compareDate = getDateFromOneYearAgo()
	df_i = df_i[df_i['date'] > compareDate]
	df_i = df_i.dropna(subset = ['score']) #filter out scores of 0, nan, ect.
	df_i = df_i.sort_values("date", ascending = True)
	df_i = pandas.DataFrame({'business_id': df_i["business_id"],'score': df_i["score"],'date': df_i["date"], 'description':df_i["description"], 'type':df_i["type"]}).to_csv('inspections copy.csv')
				
				
# check if files are up to date otherwise update them
# run this section first and save the filtered data as a new csv
# read files
df_b = pandas.read_csv("businesses copy.csv")#, nrows = 10)
df_i = pandas.read_csv("inspections copy.csv")

#filter data
filterDataFile_Businesses(df_b)
#df_i["date"] = reformatDate(df_i)
filterDataFile_Inspections(df_i)

#create dictionaries
businessDict = creat_Dict_from_CSV("businesses copy.csv")
inspectionDict = creat_Dict_from_CSV("inspections copy.csv")
mergedDict = merge_dictionaries()

#Folium Mapping Section
map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df_b['latitude'].mean(),df_b['longitude'].mean()],zoom_start= 13)

fg = folium.FeatureGroup(name="Restuarants")

for index in range(len(mergedDict)):
	lat = mergedDict[index]['latitude']
	lon = mergedDict[index]['longitude']
	score = mergedDict[index]['score']

	fg.add_child(folium.Marker(location = [lat,lon], popup = folium.Popup(getPopupInfo(mergedDict[index]), max_width=175, min_height=200), icon = folium.Icon(color = color(score), icon_color = "white")))
	
map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')