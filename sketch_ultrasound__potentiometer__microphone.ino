
int analogValue = 0;    // select the input pin for the potentiometer
const int TRIG_PIN = 12
const int ECHO_PIN = 13;
 
void setup() {
  // initialize serial communication:
  Serial.begin(9600);
 
  pinMode(TRIG_PIN,OUTPUT);
  pinMode(ECHO_PIN,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop()
{
   unsigned long startMillis= millis();  // Start of sample window
   unsigned int peakToPeak = 0;   // peak-to-peak level

   unsigned int signalMax = 0;
   unsigned int signalMin = 1024;

   long duration, distanceCm, distanceIn;
 
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN,HIGH);
 
  // convert the time into a distance
  distanceCm = duration / 29.1 / 2 ;
  distanceIn = duration / 74 / 2;
 
  if (distanceCm <= 0){
    Serial.println("Out of range");
  }
  else {
    Serial.print("The distance of the obstacle is");
     Serial.print(distanceCm);
    Serial.print("cm");
    Serial.println();
  }


  while (millis() - startMillis < sampleWindow)
   {
      sample = analogRead(0);
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
if (volts > 0.6)
{
   digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
}
 else
digitalWrite(LED_BUILTIN, LOW); 
}

//potentiometer

analogValue = analogRead(0);
Serial.println(analogValue);

  delay(1000);
}
