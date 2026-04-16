#include <TinyWireS.h>

// byte pinSense = 4;
// byte pinSense = PIN_PB4;
byte pinSense = A2;
byte pinThresh = A3;
const byte I2C_SLAVE_ADDRESS = 0x15;

volatile byte highByte = 0;
volatile byte lowByte = 0;
byte hi = 0;
byte lo = 0;
uint16_t rawData;

void requestISR()
{
  TinyWireS.write(highByte);
  TinyWireS.write(lowByte);
}

void setup() {
  analogReference(DEFAULT);
  TinyWireS.begin(I2C_SLAVE_ADDRESS);
  TinyWireS.onRequest(requestISR);

  pinMode(pinSense, INPUT_PULLUP);
}

void loop()
{
  TinyWireS_stop_check();

  rawData = analogRead(pinSense);
  hi = (rawData >> 8) & 0xFF;
  lo = rawData & 0xFF;
  noInterrupts();
  highByte = hi;
  lowByte = lo;
  interrupts();

}
