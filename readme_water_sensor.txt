# Water Sensor + Arduino UNO + Raspberry Pi 5 Setup Guide

This guide will walk you through connecting a water/moisture sensor to an Arduino UNO and monitoring the data with a Raspberry Pi 5.

## Hardware Requirements

- Arduino UNO board
- Analog water sensor (soil moisture sensor or water level sensor)
- USB cable to connect Arduino to Raspberry Pi
- 3 jumper wires
- Optional: small breadboard for easier connections

## Water Sensor Types

This guide works with several types of water sensors:

1. **Soil moisture sensor** - Has probes that measure soil conductivity
2. **Water level sensor** - Has exposed conductive tracks to detect water level
3. **Rain sensor** - Detects presence of water on its surface
4. **Water leak detector** - Similar to level sensors but designed for leak detection

## Arduino Connection Instructions

### Step 1: Identify Your Water Sensor Pins

Most analog water sensors have 3 pins:
- VCC (Power) - Connect to 5V
- GND (Ground) - Connect to GND
- OUT/SIGNAL/DATA - Connect to analog pin A0

![Water Sensor Pins Diagram]

### Step 2: Connect the Sensor to Arduino UNO

1. **Power Connection**:
   - Connect the VCC pin of water sensor to the 5V pin on Arduino UNO
   - Use a red jumper wire

2. **Ground Connection**:
   - Connect the GND pin of water sensor to any GND pin on Arduino UNO
   - Use a black jumper wire

3. **Signal Connection**:
   - Connect the OUT/SIGNAL/DATA pin of water sensor to analog pin A0 on Arduino UNO
   - Use a yellow or blue jumper wire

### Wiring Diagram (Text Version)

```
Water Sensor Module         Arduino UNO
----------------           ----------
VCC (+) ------------------ 5V
GND (-) ------------------ GND
OUT/SIGNAL --------------- Analog Pin A0
```

## Testing Your Connection

After connecting the hardware and uploading the Arduino sketch:

1. Open the Arduino Serial Monitor (Tools > Serial Monitor)
2. Set the baud rate to 9600
3. You should see moisture percentage values (0-100%)
4. Test the sensor by:
   - For soil moisture sensors: Place it in dry soil, then wet soil
   - For water level sensors: Keep it dry, then dip in water
   - For rain sensors: Keep it dry, then apply drops of water

## Calibration Tips

The Arduino sketch includes default values for dry (0) and wet (1023) readings, but you may need to calibrate for your specific sensor:

1. To find your DRY_VALUE:
   - Keep the sensor completely dry
   - Read the raw value from Serial Monitor (uncomment Option 1 in the sketch)
   - Note this value

2. To find your WET_VALUE:
   - Submerge the sensor in water (or place in very wet soil)
   - Read the raw value from Serial Monitor
   - Note this value

3. Update the DRY_VALUE and WET_VALUE constants in the Arduino sketch for more accurate readings

## Setting Up the Raspberry Pi

After the Arduino is working correctly:

1. Connect the Arduino to your Raspberry Pi 5 via USB
2. Find the correct serial port:
   ```bash
   ls /dev/ttyUSB* /dev/ttyACM*
   ```
   
3. Update the SERIAL_PORT variable in the Python script if needed
4. Run the Python monitoring script:
   ```bash
   python3 water_sensor_monitor.py
   ```

## Interpreting the Results

The visualization includes three moisture level zones:

- 0-30% (Red): Dry condition
- 30-70% (Yellow): Moderate moisture
- 70-100% (Blue): Wet condition

The warning threshold is set at 70% by default - this will trigger alerts when the moisture level is high (potential flooding or leaks).

## Customizing the System

- For leak detection: Set the WARNING_THRESHOLD lower (e.g., 20%)
- For irrigation monitoring: Set the WARNING_THRESHOLD to trigger when too dry
- For flood detection: Keep the WARNING_THRESHOLD high (e.g., 80%)

## Troubleshooting

1. No Readings or Fixed Values:
   - Check all wire connections
   - Ensure the sensor is not corroded
   - Try a different analog pin (and update the code)

2. Erratic Readings:
   - Clean the sensor contacts
   - Try using a separate power supply for the Arduino
   - Add a capacitor (e.g., 100μF) between power and ground to stabilize

3. Serial Connection Issues:
   - Try different USB ports
   - Check if the Arduino is recognized:
     bash
     dmesg | grep tty
     `
   - Ensure permissions are set correctly:
     bash
     sudo usermod -a -G dialout $USER
     
     (Log out and log back in after this command)
