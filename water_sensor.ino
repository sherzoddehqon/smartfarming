/*
 * Arduino Water Sensor Reading Sketch
 * 
 * This sketch reads data from an analog water/moisture sensor
 * and sends it over the serial port to a Raspberry Pi.
 */

// Water sensor connected to analog pin A0 (BLUE WIRE), - to GRN (BLACK WIRE), + to 5V (RED WIRE)
#define WATER_SENSOR_PIN A0  

// Sample interval
const int SAMPLE_INTERVAL = 1000;  // Read sensor every 1000ms (1 second)

// Variables for mapping sensor values
const int DRY_VALUE = 0;      // Value when sensor is completely dry (adjust as needed)
const int WET_VALUE = 1023;   // Value when sensor is fully in water (adjust as needed)

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Print message to confirm setup
  Serial.println("Arduino water sensor setup complete");
  
  // Set the water sensor pin as input
  pinMode(WATER_SENSOR_PIN, INPUT);
}

void loop() {
  // Read the analog value from the water sensor (0-1023)
  int rawValue = analogRead(WATER_SENSOR_PIN);
  
  // Option 1: Send raw value (0-1023)
  // Serial.println(rawValue);
  
  // Option 2: Convert to percentage (0-100%)
  int percentValue = map(rawValue, DRY_VALUE, WET_VALUE, 0, 100);
  
  // Ensure the percentage stays within 0-100 range
  percentValue = constrain(percentValue, 0, 100);
  
  // Send the percentage value
  Serial.println(percentValue);
  
  // Wait before the next reading
  delay(SAMPLE_INTERVAL);
}
