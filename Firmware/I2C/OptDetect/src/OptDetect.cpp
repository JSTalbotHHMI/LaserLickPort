// Pulls in Arduino I2C implementation and `Wire` instance.
#include <Wire.h>
// Pulls in class declaration for `optDetect`.
#include <OptDetect.h>

// Default I2C address used when caller does not provide one.
const uint8_t OPT_DETECT_DEFAULT_ADDRESS = 0x15; // 7-bit unshifted I2C address
// Default optical threshold used after construction.
const uint16_t OPT_DETECT_DEFAULT_THRESHOLD = 500;

// Constructor initializes the class with safe defaults.
optDetect::optDetect(void)
	// Uses Arduino's primary I2C bus by default.
	: _i2cPort(&Wire),
	  // Uses the library's default detector address.
	  _i2cAddress(OPT_DETECT_DEFAULT_ADDRESS),
	  // Starts with a midpoint-like detection threshold.
	  _optThreshold(OPT_DETECT_DEFAULT_THRESHOLD)
// Empty constructor body because all work is done in initializer list.
{}

// Begin with selected I2C bus and current stored address.
boolean optDetect::begin(TwoWire &wirePort) {
	// Forwards to the overload that also accepts an address.
	return begin(wirePort, _i2cAddress);
}

// Begin with default bus and explicit I2C address.
boolean optDetect::begin(uint8_t i2cAddress) {
	// Forwards to two-argument overload using global Wire bus.
	return begin(Wire, i2cAddress);
}

// Begin with selected I2C bus and explicit device address.
boolean optDetect::begin(TwoWire &wirePort, uint8_t i2cAddress) {
	// Stores pointer to the chosen I2C bus object.
	_i2cPort = &wirePort;
	// Stores selected device address for later transactions.
	_i2cAddress = i2cAddress;

	// Initializes the selected I2C interface.
	_i2cPort->begin();

	// If the device does not acknowledge, fail initialization.
	if (isConnected() == false) return (false); // I2C comm failure

	// Reapplies current threshold value after successful connection.
	setThreshold(_optThreshold);

	// Reports successful initialization.
	return (true);
}

// Tests whether the configured slave acknowledges on I2C.
boolean optDetect::isConnected(void) {
	// Starts a transaction targeting stored slave address.
	_i2cPort->beginTransmission(_i2cAddress);
	// `0` means ACK/no error from the slave.
	return (_i2cPort->endTransmission() == 0);
}

// Reads a 16-bit optical sample from the detector.
uint16_t optDetect::getOpt(void)
{
	// Targets the slave before requesting data.
	_i2cPort->beginTransmission(_i2cAddress);
	// End transmission with repeated start; non-zero means bus/device error.
	if (_i2cPort->endTransmission(false) != 0)
	{
		// On communication failure, return zero sentinel.
		return (0);
	}

	// Requests exactly 2 bytes from the slave.
	_i2cPort->requestFrom(_i2cAddress, (uint8_t)2);
	// Only accept the sample if both bytes arrived.
	if (_i2cPort->available() >= 2)
	{
		// Reads the high byte first.
		uint16_t msb = _i2cPort->read();
		// Reads the low byte second.
		uint16_t lsb = _i2cPort->read();
		// Combines bytes into one 16-bit sample and returns it.
		return ((msb << 8) | lsb);
	}

	// If no data arrived, return zero sentinel.
	return (0);
}

// Returns the threshold currently stored in object state.
uint16_t optDetect::getThreshold(void)
{
	// Gives callers read access to detection threshold.
	return (_optThreshold);
}

// Updates threshold used by `isDetected` comparisons.
void optDetect::setThreshold(uint16_t threshold)
{
	// Stores caller-provided threshold value.
	_optThreshold = threshold;
}

// Returns whether the latest optical reading crosses threshold.
boolean optDetect::isDetected(void)
{
	// Compares live reading against configured threshold.
	if(getOpt() >= _optThreshold)
	{
		// Signal detection when reading is at or above threshold.
		return (true);
	}
	// Otherwise signal no detection.
	return (false);
}
