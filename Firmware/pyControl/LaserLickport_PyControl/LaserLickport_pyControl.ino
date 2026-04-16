#include <SoftwareSerial.h>
#include <ADCTouch.h>

// Version identifiers for release tracking.
#define FIRMWARE_NAME "LaserLickport_pyControl"
#define FIRMWARE_VERSION "0.1.0"
#define UART_PROTOCOL_VERSION 1

static const uint8_t OPT_PIN = A2;
static const uint8_t TOUCH_PIN = PB3;
static const uint8_t SOFT_RX_PIN = PB0;  // physical pin 5 (old SDA)
static const uint8_t SOFT_TX_PIN = PB2;  // physical pin 7 (old SCL)

static const unsigned long STREAM_INTERVAL_MS = 10;
static const uint8_t PACKET_START = 0xAA;
static const uint8_t DATA_MASK_OPT_RAW = 0x01;
static const uint8_t DATA_MASK_CAP_RAW = 0x02;

SoftwareSerial link(SOFT_RX_PIN, SOFT_TX_PIN);

bool sendOptRaw = true;
bool sendCapRaw = true;

uint16_t optRaw = 0;
uint16_t capRaw = 0;

unsigned long lastStreamMs = 0;

void setup() {
  link.begin(57600);
}

void loop() {
  readInputs();
  handleCommands();

  if (millis() - lastStreamMs >= STREAM_INTERVAL_MS) {
    lastStreamMs = millis();
    streamData();
  }
}

void readInputs() {
  optRaw = analogRead(OPT_PIN);
  delayMicroseconds(200);
  capRaw = ADCTouch.read(TOUCH_PIN,2);
  delayMicroseconds(200);
}

void handleCommands() {
  static char buffer[48];
  static uint8_t index = 0;

  while (link.available()) {
    char c = (char)link.read();
    if (c == '\r') {
      continue;
    }
    if (c == '\n') {
      buffer[index] = 0;
      parseCommand(buffer);
      index = 0;
      continue;
    }
    if (index < sizeof(buffer) - 1) {
      buffer[index++] = c;
    }
  }
}

void parseCommand(char *command) {
  if (command[0] == 'E') {
    int a = 0;
    int b = 0;
    if (sscanf(command, "E,%d,%d", &a, &b) == 2) {
      sendOptRaw = a != 0;
      sendCapRaw = b != 0;
      return;
    }
  }
}

void streamData() {
  uint8_t mask = 0;
  if (sendOptRaw) {
    mask |= DATA_MASK_OPT_RAW;
  }
  if (sendCapRaw) {
    mask |= DATA_MASK_CAP_RAW;
  }

  uint8_t checksum = 'D' ^ mask;

  link.write(PACKET_START);
  link.write('D');
  link.write(mask);

  if (mask & DATA_MASK_OPT_RAW) {
    writeUint16(optRaw);
    checksum ^= (uint8_t)(optRaw >> 8);
    checksum ^= (uint8_t)(optRaw & 0xFF);
  }
  if (mask & DATA_MASK_CAP_RAW) {
    writeUint16(capRaw);
    checksum ^= (uint8_t)(capRaw >> 8);
    checksum ^= (uint8_t)(capRaw & 0xFF);
  }

  link.write(checksum);
}

void writeUint16(uint16_t value) {
  link.write((uint8_t)(value >> 8));
  link.write((uint8_t)(value & 0xFF));
}
