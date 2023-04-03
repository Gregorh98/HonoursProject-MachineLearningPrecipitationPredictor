from flask import Flask, render_template, url_for;
import pickle, time, csv, datetime, serial, math;
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

app = Flask(__name__);

def testAgainstModel(dataDict):
	#Load model
	model = pickle.load(open("static/finalisedModel.sav", "rb"))

	#Test current data against model
	XNew = [[dataDict["Temperature"], dataDict["Humidity"], dataDict["Light"], dataDict["Moisture"]]]
	YNew = model.predict_proba(XNew)

	return YNew


@app.route('/')
def index():
	#Initiate serial and gather latest sensor readings
	try:
		s = serial.Serial("/dev/ttyUSB0")
		serialData = ((s.readline()).decode('utf-8'));
		print (serialData)
		s.close()
		serialArr = [];
		for x in serialData.split(","):
			serialArr.append(int(x));

		#Get current time
		currentDateTime = datetime.datetime.today();

		#Add current data to a dictionary
		dataDict = {};
		dataDict["Temperature"]		= serialArr[0];
		dataDict["Humidity"]		= serialArr[1];
		dataDict["Light"]			= serialArr[2];
		dataDict["Moisture"]		= serialArr[3];

		#Get current rainfall prediction using data dictionary of latest sensor readings

		#0 = no, 1 = yes
		prediction = testAgainstModel(dataDict)
		print(prediction)

		chanceOfRain = math.floor(prediction[0][1]*100)
		chanceOfSun  = math.floor(prediction[0][0]*100)

		print(chanceOfRain, chanceOfSun)

		if chanceOfRain > chanceOfSun:
			pred = "Yes"
			cert=chanceOfRain
			imageName="rainYes"
		else:
			pred = "No"
			cert=chanceOfSun
			imageName="rainNo"

		return render_template("index.html", time = datetime.datetime.now(), temp=dataDict["Temperature"], humid = dataDict["Humidity"], light=dataDict["Light"], moist = dataDict["Moisture"], certainty = cert, predict = pred, imageName = imageName)
	except:
		return("Unable to access sensors, please run rws.sh!")


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

