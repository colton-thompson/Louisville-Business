import folium
import pandas

df_b = pandas.read_csv("businesses.csv")#, nrows = 100)
df_i = pandas.read_csv("inspections.csv")


#filter data
df_b = df_b[df_b['latitude']!=0.0]
df_b = df_b[df_b['longitude']!=0.0]
df_b = df_b[df_b.phone_number.notnull()]
df_b = df_b.sort_values("business_id", ascending = False)
print(df_b.head(n=10))

newDateList = []
def reformatDate(df):
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

df_i = df_i[df_i['score']!=0]
#df_i = df_i['type'].str.contains("routine")

df_i["date"] = reformatDate(df_i)
df_i = df_i.sort_values("business_id", ascending = False)
print(df_i.head(n=10))

map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start= 13)

business_id_List = []

def getPopupInfo(name, address):
	score = attachScore()
	popup = name + "<br>Address: " + addy +"<br>Score: " + str(score)
	return popup
	
def attachScore():
	for index in df_b['business_id']:
		if (index not in business_id_List):
			for index2 in df_i['business_id']:
				if (index == index2):
					#print(df_i['score'])	
					score = df_i['score']
					business_id_List.append(index)
					return score
		else:
			return -1;
	
fg = folium.FeatureGroup(name="Restuarants")
for la,lo,name,addy in zip(df_b["latitude"],df_b["longitude"],df_b["name"], df_b["address"]):
	try:
	#scooter_fg.add_child(folium.CircleMarker(location=[la,lo], radius = 5, color = 'black', weight = 4, popup = "Scooter: " + bikeID))
		fg.add_child(folium.Marker(location=[la,lo],popup=(folium.Popup(getPopupInfo(name, addy),max_width=150,min_height=200)),icon=folium.Icon(color="red", icon_color='white')))
	except TypeError:
		raise
		
df_b = pandas.DataFrame({'business_id': df_b["business_id"],'name': df_b["name"],'address': df_b["address"], 'city':df_b["city"], 'state':df_b["state"], 'postal_code':df_b["postal_code"], 'latitude':df_b["latitude"],'longitude':df_b["longitude"], 'phone_number':df_b["phone_number"]}).to_csv('test.csv')

map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')