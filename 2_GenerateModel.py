import time
startTime = time.time()

# make predictions
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle, warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def cleanData(dataset):
	#Remove all data where rain couldnt be identified
	dataset = dataset[dataset.Rain != "TELEMETRYLOST"]
	
	#Remove all data where temp out of bounds
	dataset = dataset[dataset.Temp <= 20]
	dataset = dataset[dataset.Temp >= -5]
	
	#Remove all data where humidity out of bounds
	dataset = dataset[dataset.Humidity <= 80]
	dataset = dataset[dataset.Humidity >= 10]
	
	#Remove all data where light level out of bounds
	dataset = dataset[dataset.Light <= 60]
	dataset = dataset[dataset.Light >= 0]
	
	#Remove all data where soil moisture out of bounds
	dataset = dataset[dataset.Moisture <= 100]
	dataset = dataset[dataset.Moisture >= 0]
	
	#Remove date and time columns
	dataset = dataset.drop(["Time", "Date"], axis=1)
	
	return dataset


"""=== Train Model ==="""
print("--- Updating Model ---")
# Load dataset
url = "/home/pi/weatherApp/static/dataset.csv"
names = ['Date','Time','Temp', 'Humidity', 'Light', 'Moisture', 'Rain']
dataset = read_csv(url, names=names)

dataset = cleanData(dataset)


#Split-out validation dataset
array = dataset.values
X = array[:,0:4]
y = array[:,4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.40, random_state=1)


# Make predictions on validation dataset
model = LinearDiscriminantAnalysis()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)


# Evaluate predictions
print("\nAccuracy: %s percent" % (str(accuracy_score(Y_validation, predictions)*100)[:5]))
print("\nConfusion Matrix:\n", confusion_matrix(Y_validation, predictions))
print("\nClassification Report:\n", classification_report(Y_validation, predictions))

#save model
filename = '/home/pi/weatherApp/static/finalisedModel.sav'
pickle.dump(model, open(filename, 'wb'), 2)

endTime = time.time()
generationTime = endTime-startTime
print("Time taken to generate model: %.2f seconds" % (generationTime))
