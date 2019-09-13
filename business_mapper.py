import sys
import csv
import pprint
import folium 
import pandas
import branca
from datetime import date
from colorama import Fore, Back, Style 

# TODO make dynamic html boxes based on size of input

def reformatDate(date):
	date = str(date)
	year = date[0:4]
	month = date[4:6]
	day = date[6:8]
	newDate = month + "/" + day + "/" + year 
	return newDate
	
def reformatCaps(name):
	nameList = name.split()
	newName = ""
	# if first value is char, keep it uppercase, else return the symbol
	# for any value after 1st, make it lowercase if it is char, else return the symbol
	for index in nameList:
		newName += (str(index[0:1]) + str(index[1:]).lower() + ' ')
	return newName
	
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
	
# check score to determine color 	
def color(score): 
	score = float(score)
	if score >= 90.0: 
		col = 'green'
	elif score >= 80.0: 
		col = 'blue'
	else:
		col='red'
	return col 

# compare two dictionaries and merge necessary content into one
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
	
def getHTML(data):
	#TODO add in reformat name like we have for date
	# Takes in variable and outputs string into an HTML format
	# concat the strings and then return
	name = "<b><p style= \"font-size: 13px; display: inline;\">Name: </b>" + reformatCaps(data['name']) + "</p>" 
	address = "<br><b><p style=\"font-size: 13px; display: inline;\">Address: </b>" + reformatCaps(data['address']) + "</p>"
	score = "<br><b><p style= \"font-size: 13px; display: inline;\">Score: </b><p style=\"color: " + color(data['score']) +";font-size: 13px; display: inline;\">" + data['score'] +"</p>"
	date = "<br><b><p style=\"font-size: 13px; display: inline;\">Last checked: </b>" + reformatDate(data['date']) + "</p>"
	
	details = name + address + score + date
	return details
				
# check if files are up to date otherwise update them
# run this section first and save the filtered data as a new csv
# read files
df_b = pandas.read_csv("businesses copy.csv")#, nrows = 10)
df_i = pandas.read_csv("inspections copy.csv")

#filter data
filterDataFile_Businesses(df_b)
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
	
	#TODO consider function to change width based on size of the name input (considertion)
	iframe = branca.element.IFrame(html = getHTML(mergedDict[index]), width=250, height=75)
	
	popup = folium.Popup(iframe, max_width=250, min_height=200)	
	icon = folium.Icon(color = color(score), icon_color = "white")
	fg.add_child(folium.Marker(location = [lat,lon], popup = popup, icon = icon))
	
	
map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')