// Prevents multiple inclusion of this header in one compile unit.
#ifndef OPTDETECT_H
// Defines the include guard macro once this file is included.
#define OPTDETECT_H

// If compiling in a modern Arduino core, include Arduino.h.
#if defined(ARDUINO) && ARDUINO >= 100
// Arduino base types and helpers (modern cores).
#include "Arduino.h"
// Otherwise fall back to legacy Arduino core header.
#else
// Arduino base types and helpers (older cores).
#include "WProgram.h"
// Ends Arduino-version conditional include.
#endif

// Pulls in the I2C/TWI interface type `TwoWire` and global `Wire` object.
#include <Wire.h>

// Declares the optical detector interface class.
class optDetect {
	// Public API callable by sketches.
	public:
		// Constructor initializes defaults in the .cpp file.
		optDetect();
		
		// Starts I2C using a selected bus (defaults to global `Wire`).
		boolean begin(TwoWire &wirePort = Wire);
		// Starts I2C and sets a specific slave address.
		boolean begin(TwoWire &wirePort, uint8_t i2cAddress);
		// Starts I2C using default `Wire` but with explicit slave address.
		boolean begin(uint8_t i2cAddress);
		// Probes the device to confirm I2C connectivity.
		boolean isConnected(void);
		
		// Reads the current 16-bit optical value from the sensor slave.
		uint16_t getOpt(void);
		// Returns the currently configured detection threshold.
		uint16_t getThreshold(void);
		// Updates the detection threshold used by `isDetected`.
		void setThreshold(uint16_t threshold);
		// Returns true when `getOpt()` is at or above threshold.
		boolean isDetected();
		
	// Internal state hidden from external users.
	private:
		// Active I2C port used for all transactions.
		TwoWire *_i2cPort;
		// Current 7-bit I2C address of the detector slave.
		uint8_t _i2cAddress;
		// Cached threshold used for detection decision logic.
		uint16_t _optThreshold;
};
// Closes include guard started at top of file.
#endif
