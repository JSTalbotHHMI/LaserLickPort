// Version identifiers for release tracking.
#define FIRMWARE_NAME "LaserLickport_Standalone"
#define FIRMWARE_VERSION "0.1.0"

byte pinSense = A2;
byte pinThresh = A1;
byte pinTTL = 0;

uint16_t rawData;
uint16_t thresh;

void setup() {
  analogReference(DEFAULT);

  pinMode(pinSense, INPUT_PULLUP);
  pinMode(pinThresh, INPUT_PULLUP);
  pinMode(pinTTL, OUTPUT);
}

void loop()
{

  rawData = analogRead(pinSense);
  thresh = analogRead(pinThresh);
  if(rawData>=thresh)
  {
    digitalWrite(pinTTL,HIGH);
  } else {
    digitalWrite(pinTTL,LOW);
  }

  delayMicroseconds(20);
}
