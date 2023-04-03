#include <dht.h>

dht DHT;
#define DHT11_PIN 7
#define lghtPin A0
#define soilPin A1

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  //--- Get data from sensors ---
  int chk = DHT.read11(DHT11_PIN); //Gets data from temperature and humidity sensor
  
  int temp = DHT.temperature;
  int hmid = DHT.humidity;
  int lght = map(analogRead(lghtPin), 0, 1024, 0, 100);
  int soil = map(analogRead(soilPin), 0, 1024, 100, 0);

  //--- Put data in array ---
  int data[4] = {temp, hmid, lght, soil};
  for (int i=0; i<4; i++)
  {
    Serial.print(data[i]);
    if (i<3)
    {
      Serial.print(",");
    }
  }

  Serial.println();
  
  //Serial.print("Temperature Value: ");
  //Serial.println(data[0]);
  //Serial.print("Humidity Value: ");
  //Serial.println(data[1]);
  //Serial.print("Light Level: ");
  //Serial.println(data[2]);
  //Serial.print("Soil Moisture Level: ");
  //Serial.println(data[3]);
  //Serial.println("\n\n");
    
  delay(300000); //300,000 == 5 mins
}
