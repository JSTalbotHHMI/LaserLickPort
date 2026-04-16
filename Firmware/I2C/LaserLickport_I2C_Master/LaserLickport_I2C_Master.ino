#include <OptDetect.h>

optDetect opticalLickdetect;

const uint8_t OPT_DETECT_ADDRESS = 0x15;
uint16_t opticalThreshold = 500;

void setup() {
  Serial.begin(115200);
  while(!Serial)
  {
    delay(20);
  }

  Wire.begin();
  delay(20);

  opticalLickdetect.begin(OPT_DETECT_ADDRESS);

  delay(50);

  if(!opticalLickdetect.isConnected())
  {
    Serial.println("Detector not found.");
    while(1)
    {
      delay(20);
    }
  }

  Serial.println("Detector found!");
  delay(500);
  opticalLickdetect.setThreshold(opticalThreshold);
  delay(500);

}

void loop() {
  // Serial.print(opticalLickdetect.isDetected());
  // Serial.print(", ");
  Serial.print(0);
  Serial.print(", ");
  Serial.print(1024);
  Serial.print(", ");
  Serial.println(opticalLickdetect.getOpt());
  delay(5);
}
