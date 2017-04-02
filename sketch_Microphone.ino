#include <SparkFunTMP102.h>

/****************************************
Example Sound Level Sketch for the 
Adafruit Microphone Amplifier
****************************************/

const int sampleWindow = 50; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;
int analogValue = 2;    // select the input pin for the potentiometer
const int TRIG_PIN = 12;
const int ECHO_PIN = 8;
//int led = 8;
const int ALERT_PIN = A3;

TMP102 sensor0(0x48);


void setup() 
{
   Serial.begin(9600);
   
 
  pinMode(TRIG_PIN,OUTPUT);
   pinMode(LED_BUILTIN, OUTPUT);

   pinMode(ALERT_PIN,INPUT);  // Declare alertPin as an input
  sensor0.begin();  // Join I2C bus

  // Initialize sensor0 settings
  // These settings are saved in the sensor, even if it loses power

  // set the number of consecutive faults before triggering alarm.
  // 0-3: 0:1 fault, 1:2 faults, 2:4 faults, 3:6 faults.
  sensor0.setFault(0);  // Trigger alarm immediately

  // set the polarity of the Alarm. (0:Active LOW, 1:Active HIGH).
  sensor0.setAlertPolarity(1); // Active HIGH

  // set the sensor in Comparator Mode (0) or Interrupt Mode (1).
  sensor0.setAlertMode(0); // Comparator Mode.

  // set the Conversion Rate (how quickly the sensor gets a new reading)
  //0-3: 0:0.25Hz, 1:1Hz, 2:4Hz, 3:8Hz
  sensor0.setConversionRate(2);

  //set Extended Mode.
  //0:12-bit Temperature(-55C to +128C) 1:13-bit Temperature(-55C to +150C)
  sensor0.setExtendedMode(0);

  //set T_HIGH, the upper limit to trigger the alert on
  sensor0.setHighTempF(85.0);  // set T_HIGH in F
  //sensor0.setHighTempC(29.4); // set T_HIGH in C

  //set T_LOW, the lower limit to shut turn off the alert
  sensor0.setLowTempF(84.0);  // set T_LOW in F
  //sensor0.setLowTempC(26.67); // set T_LOW in C
}


void loop() 
{
   unsigned long startMillis= millis();  // Start of sample window
   unsigned int peakToPeak = 0;   // peak-to-peak level

   unsigned int signalMax = 0;
   unsigned int signalMin = 1024;

   // collect data for 50 mS
   while (millis() - startMillis < sampleWindow)
   {
      sample = analogRead(1);
      if (sample < 1024)  // toss out spurious readings
      {
         if (sample > signalMax)
         {
            signalMax = sample;  // save just the max levels
         }
         else if (sample < signalMin)
         {
            signalMin = sample;  // save just the min levels
         }
      }
   }
   peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
   double volts = (peakToPeak * 5.0) / 1024;  // convert to volts
   Serial.println(volts);
if(volts > 3)
{
  digitalWrite(LED_BUILTIN, HIGH);
}
else
{
    digitalWrite(LED_BUILTIN, LOW);
}
    
 long duration, distanceCm;
 
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN,HIGH);
 
  // convert the time into a distance
  distanceCm = duration / 29.1 / 2 ;
 
 
  if (distanceCm <= 0){
    Serial.println("Out of range");
  }
  else {
    Serial.print("The distance of the obstacle is ");
     Serial.print(distanceCm);
    Serial.print(" cm");
    Serial.println();
  } 

analogValue = analogRead(2);
Serial.print("The potentiometer value is "); //Value between 0 to 1023
Serial.println(analogValue);

float temperature;
  boolean alertPinState, alertRegisterState;

  // Turn sensor on to start temperature measurement.
  // Current consumtion typically ~10uA.
  sensor0.wakeup();

  // read temperature data
  temperature = sensor0.readTempF();
  temperature = (temperature-32)/1.8;
  //temperature = sensor0.readTempC();

  // Check for Alert
  alertPinState = digitalRead(ALERT_PIN); // read the Alert from pin
  alertRegisterState = sensor0.alert();   // read the Alert from register

  // Place sensor in sleep mode to save power.
  // Current consumtion typically <0.5uA.
  sensor0.sleep();

  // Print temperature and alarm state
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" C");
  Serial.println();
  Serial.println();
 delay(100);

 
}
