#Import modules
import serial, datetime, requests, json, terminaltables;

print("Now testing sensors!\n");

#Set variable s to the serial connection
s = serial.Serial("/dev/ttyUSB0");

def checkRain():
	response = (requests.get("http://api.openweathermap.org/data/2.5/weather?appid=2b1b0605d48f3ddc3ed3b0a17bbd6b55&q=roslin,scotland")).json();
	z = response["weather"];
	weather_description = z[0]["description"];
	print ("Current Weather = ", weather_description)

	if "RAIN" in (str(weather_description)).upper():
		return 1;
	else:
		return 0;


#Get data from serial and add it to a list
serialData = ((s.readline()).decode('utf-8'));
serialArr = [];
for x in serialData.split(","):
	serialArr.append(int(x));

#Get current time
currentDateTime = datetime.datetime.today();

#Add data to a 2d array for display as a table
datadict = []
datadict.append(["Date", "Time", "Temperature", "Humidity", "Light Level", "Soil Moisture Level"])
datadict.append([currentDateTime.strftime("%d/%m/%y"), currentDateTime.strftime("%H:%M"), serialArr[0], serialArr[1], serialArr[2], serialArr[3]])



#dataDict = {};
#dataDict["Date"]			= currentDateTime.strftime("%d/%m/%y");
#dataDict["Time"]			= currentDateTime.strftime("%H:%M");
#dataDict["Temperature"]			= serialArr[0];
#dataDict["Humidity"]			= serialArr[1];
#dataDict["Light"]			= serialArr[2];
#dataDict["Moisture"]			= serialArr[3];
try:
	raining		= checkRain();
except:
	raining		= "TELEMETRY LOST";

#Output the dataDict to the console
#for x in dataDict.keys():
#	print("%s		= %s" % (x, dataDict[x]))

table = terminaltables.AsciiTable(datadict)
print(table.table)
print("\n")
