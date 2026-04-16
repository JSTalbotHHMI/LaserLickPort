#include <Wire.h>
#include <OptDetect.h>

optDetect detector;

const uint8_t OPT_DETECT_ADDRESS = 0x15;
const uint16_t DETECTION_THRESHOLD = 500;
const unsigned long PRINT_INTERVAL_MS = 100;

unsigned long lastPrintMs = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  if (!detector.begin(OPT_DETECT_ADDRESS)) {
    Serial.println("OptDetect device not found on I2C.");
    while (1) {
      delay(100);
    }
  }

  detector.setThreshold(DETECTION_THRESHOLD);

  Serial.println("OptDetect connected.");
  Serial.print("Threshold: ");
  Serial.println(detector.getThreshold());
  Serial.println("optRaw,detected");
}

void loop() {
  if (millis() - lastPrintMs < PRINT_INTERVAL_MS) {
    return;
  }

  lastPrintMs = millis();

  uint16_t optRaw = detector.getOpt();
  bool detected = detector.isDetected();

  Serial.print(optRaw);
  Serial.print(",");
  Serial.println(detected ? 1 : 0);
}
