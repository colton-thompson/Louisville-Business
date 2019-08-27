#reformat businesses date into readable format
import pandas as pd


#df = pd.read_csv("ODP_New_Reg.csv")
df = pd.read_csv("dateTest.csv")


newDateList = []

for date in df["date"]:
	year = str(date)
	year = (year[0:4])

	month = str(date)
	month = month[5:6]
	
	day = str(date)
	day = day[7:8]
	
	newDate = year + "-" + month + "-" + day
	newDateList.append(newDate)
	
df["date"] = newDateList
	
df = pd.DataFrame({'date': newDateList, 'business_id':df["business_id"]})
df.to_excel('businesses.xlsx')
