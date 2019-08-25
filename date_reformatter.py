#reformat businesses date into readable format
import pandas as pd


#df = pd.read_csv("ODP_New_Reg.csv")
df = pd.read_csv("businesses.csv")

for co in df:
	

newDateList = []
'''
for date in df[" Commence Date"]:
	year = str(date)
	year = (year[0:4])

	month = str(date)
	month = month[5:6]
	
	day = str(date)
	day = day[7:8]
	
	newDate = year + "-" + month + "-" + day
	newDateList.append(newDate)
	
	
df = pd.DataFrame({'Date': newDateList, 'Business Name':df["Business Name"]})
df.to_excel('businesses.xlsx')'''
