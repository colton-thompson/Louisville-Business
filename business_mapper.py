import folium
import pandas

df_b = pandas.read_csv("businesses.csv")#, nrows = 100)
#filter data

df_b = df_b[df_b['latitude']!=0.0]
df_b = df_b[df_b['longitude']!=0.0]
df_b = df_b[df_b.phone_number.notnull()]
df_b = df_b.sort_values("business_id", ascending = False)
print(df_b.head(n=10))


#df_b.to_excel('businesses.xlsx')

map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start= 13)

def getPopupInfo(name, address):
	popup = name + "\nAddress: " + addy
	return popup
	
fg = folium.FeatureGroup(name="Restuarants")
for la,lo,name,addy in zip(df_b["latitude"],df_b["longitude"],df_b["name"], df_b["address"]):
	try:
	#scooter_fg.add_child(folium.CircleMarker(location=[la,lo], radius = 5, color = 'black', weight = 4, popup = "Scooter: " + bikeID))
		fg.add_child(folium.Marker(location=[la,lo],popup=(folium.Popup(getPopupInfo(name, addy))),icon=folium.Icon(color="red", icon_color='white')))
	except TypeError:
		raise
		
df_b = pandas.DataFrame({'business_id': df_b["business_id"],'name': df_b["name"],'address': df_b["address"], 'city':df_b["city"], 'state':df_b["state"], 'postal_code':df_b["postal_code"], 'latitude':df_b["latitude"],'longitude':df_b["longitude"], 'phone_number':df_b["phone_number"]}).to_csv('test.csv')

map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')