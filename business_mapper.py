import folium
import pandas

df = pandas.read_csv("businesses.csv", nrows = 100)
	
map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start= 13)

def getPopupInfo(name, address):
	popup = name + "\nAddress: " + addy
	return popup
	
fg = folium.FeatureGroup(name="Restuarants")
for la,lo,name,addy in zip(df["latitude"],df["longitude"],df["name"], df["address"]):
	#scooter_fg.add_child(folium.CircleMarker(location=[la,lo], radius = 5, color = 'black', weight = 4, popup = "Scooter: " + bikeID))
	fg.add_child(folium.Marker(location=[la,lo],popup=(folium.Popup(getPopupInfo(name, addy))),icon=folium.Icon(color="red",icon_color='white')))

map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')