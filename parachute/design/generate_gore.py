#include <SPI.h>
#include "SdFat.h"

#define DT 16         // HX711 Data pin
#define SCK 17        // HX711 Clock pin
#define SD_CS 5       // SD Card CS pin

// Globals
SdFat sd;
SdFile logFile;

float scaleFactor = -4.47823;
long tareOffset = 44300;
int fileCounter = 1;
String currentFileName;

// -------------- SETUP --------------
void setup() {
  Serial.begin(115200);
  pinMode(DT, INPUT);
  pinMode(SCK, OUTPUT);

  if (!sd.begin(SD_CS, SD_SCK_MHZ(25))) {
    Serial.println("SD initialization failed.");
    sd.initErrorPrint(&Serial);
    while (1); // Halt if SD card fails
  } else {
    Serial.println("SD card ready.");
    
    while (true) {
      currentFileName = "thrust_log_" + String(fileCounter) + ".txt";
      if (!sd.exists(currentFileName.c_str())) {
        break;
      }
      fileCounter++;
    }
    Serial.print("Logging to: ");
    Serial.println(currentFileName);

    if (logFile.open(currentFileName.c_str(), O_WRITE | O_CREAT | O_TRUNC)) {
      logFile.println("Millis\tRawValue\tWeight(g)");
      logFile.close();
    } else {
      Serial.println("Failed to create new log file");
    }
  }

  Serial.println("Send 'tare' to zero the scale.");
  Serial.println("Send 'calibrate X' where X = known weight (g or kg).");
  Serial.println("Send 'reset' to create a new log file.");
}

// -------------- MAIN LOOP --------------
void loop() {
  long raw = readHX711();
  float weight = (raw - tareOffset) / scaleFactor;

  Serial.print("Raw: ");
  Serial.print(raw);
  Serial.print(" | Weight: ");
  Serial.print(weight, 2);
  Serial.println(" g");

  if (!logFile.open(currentFileName.c_str(), O_RDWR | O_AT_END)) {
    Serial.println("Can't open " + currentFileName);
    sd.errorPrint(&Serial);
  } else {
    logFile.print(millis());
    logFile.print('\t');
    logFile.print(raw);
    logFile.print('\t');
    logFile.println(weight, 2);
    logFile.close();
  }

  handleSerialInput();
  delay(500);
}

// -------------- HX711 READING --------------
long readHX711() {
  while (digitalRead(DT));

  long value = 0;
  for (int i = 0; i < 24; i++) {
    digitalWrite(SCK, HIGH);
    delayMicroseconds(1);
    value = (value << 1) | digitalRead(DT);
    digitalWrite(SCK, LOW);
    delayMicroseconds(1);
  }

  if (value & 0x800000) {
    value |= 0xFF000000;
  }

  digitalWrite(SCK, HIGH); delayMicroseconds(1);
  digitalWrite(SCK, LOW); delayMicroseconds(1);

  return value;
}

// -------------- TARE FUNCTION --------------
void tare() {
  tareOffset = readHX711();
  Serial.println("Tare complete.");

  if (logFile.open("calibration.txt", O_WRITE | O_CREAT | O_TRUNC)) {
    logFile.print("Tare: ");
    logFile.println(tareOffset);
    logFile.close();
  } else {
    Serial.println("Failed to write tare");
  }
}

// -------------- CALIBRATION FUNCTION --------------
void calibrate(float knownWeight) {
  long raw = readHX711();
  scaleFactor = (raw - tareOffset) / knownWeight;

  Serial.print("Calibrated. New scale factor: ");
  Serial.println(scaleFactor, 5);

  if (logFile.open("calibration.txt", O_WRITE | O_CREAT | O_TRUNC)) {
    logFile.print("Tare: ");
    logFile.println(tareOffset);
    logFile.print("ScaleFactor: ");
    logFile.println(scaleFactor, 5);
    logFile.close();
  } else {
    Serial.println("Failed to write calibration");
  }
}

// -------------- SERIAL COMMANDS --------------
void handleSerialInput() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("tare")) {
      tare();
    } else if (input.startsWith("calibrate")) {
      float known = input.substring(10).toFloat();
      if (known > 0) calibrate(known);
      else Serial.println("Use: calibrate <weight>");
    } else if (input.equalsIgnoreCase("reset")) {
      fileCounter++;
      currentFileName = "thrust_log_" + String(fileCounter) + ".txt";
      
      if (logFile.open(currentFileName.c_str(), O_WRITE | O_CREAT | O_TRUNC)) {
        logFile.println("Millis\tRawValue\tWeight(g)");
        logFile.close();
        Serial.println("New log file: " + currentFileName);
      } else {
        Serial.println("Failed to create new log file");
        fileCounter--;
      }
    }
  }
}
