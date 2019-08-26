import folium
import pandas

df_b = pandas.read_csv("businesses.csv")#, nrows = 100)
df_b = df_b.sort_values("business_id", ascending = False)
print(df_b.head(n=10))

map = folium.Map(location=[38.217090,-85.742117],zoom_start= 13)
#map = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start= 13)

def getPopupInfo(name, address):
	popup = name + "\nAddress: " + addy
	return popup
	
fg = folium.FeatureGroup(name="Restuarants")
for la,lo,name,addy in zip(df_b["latitude"],df_b["longitude"],df_b["name"], df_b["address"]):
	#scooter_fg.add_child(folium.CircleMarker(location=[la,lo], radius = 5, color = 'black', weight = 4, popup = "Scooter: " + bikeID))
	fg.add_child(folium.Marker(location=[la,lo],popup=(folium.Popup(getPopupInfo(name, addy))),icon=folium.Icon(color="red", icon_color='white')))

map.add_child(fg)

map.add_child(folium.LayerControl())

map.save(outfile = 'map.html')