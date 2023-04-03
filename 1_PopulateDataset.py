import serial, csv, datetime, time

""" --- Check Rain Function --- """
def checkRain():
	#Import libraries
	import json, requests

	#Get current weather
	response = (requests.get("http://api.openweathermap.org/data/2.5/weather?appid=###REDACTEDFORGITHUB###&q=roslin,scotland")).json();

	#Get current weather description
	z = response["weather"];
	weather_description = z[0]["description"];

	#Return the current rain boolean
	if "RAIN" in (str(weather_description)).upper():
		return 1;
	else:
		return 0;

""" === Collect Dataset Loop === """
while True:
	#Get current weather data from serial
	s = serial.Serial("/dev/ttyUSB0")
	serialData = ((s.readline()).decode('utf-8'));
	s.close()

	#Split and format weather data
	serialArr = [];
	for x in serialData.split(","):
		serialArr.append(int(x));

	#Get current time
	currentDateTime = datetime.datetime.today();

	#Add data to a dictionary
	dataDict = {};
	dataDict["Date"]			= currentDateTime.strftime("%d/%m/%y");
	dataDict["Time"]			= currentDateTime.strftime("%H:%M");
	dataDict["Temperature"]		= serialArr[0];
	dataDict["Humidity"]		= serialArr[1];
	dataDict["Light"]			= serialArr[2];
	dataDict["Moisture"]		= serialArr[3];
	try:
		dataDict["Raining"]		= checkRain();
	except:
		dataDict["Raining"]		= "TELEMETRYLOST";

	#Append the data to the dataset
	with open("/home/pi/weatherApp/static/dataset.csv", "a", newline="") as f:
		writer = csv.DictWriter(f, fieldnames = dataDict.keys());
		writer.writerow(dataDict);
	
	print("Data added to file!")
	
	#Wait 5 minutes before recording next entry
	time.sleep(300)
