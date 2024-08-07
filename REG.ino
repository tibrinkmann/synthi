/***************************************************************************

Initialisierung und Konfigration des MPU9250, soeiw Auslese von Pitch und Roll über Beispielskript MPU9250_pitch_and_roll aus der Bibliothek MPU9250_WE von Wolfgang Ewald

***************************************************************************/

#include <MPU9250_WE.h>
#include <Wire.h>
#include "BluetoothSerial.h"
#define MPU9250_ADDR 0x68

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;

/* Initialisierung der feststehenden Variablen */
/* I2C Pins */
const int sda = 0;
const int scl = 4;
/* LED Anzeige  AKTUELL UNGENUTZT! */
const int led0 = 12;
const int led1 = 14;
const int led2 = 27;
const int led3 = 26;
const int led4 = 25;
const int led5 = 33;
const int led6 = 32;
const int led7 = 19;
const int led8 = 23;
const int led9 = 18;
const int led10 = 05;
const int led11 = 17;
const int led12 = 16;
const int LEDs[13] = {led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12};
/* Bedienelemente und Kontrollleds */
const int statled = 13;
const int called = 22;
const int statbtn = 15;
const int calbtn = 02;
/* Lagesensor */
MPU9250_WE myMPU9250 = MPU9250_WE(MPU9250_ADDR);

void setup() {
  /* Initialisierung der I/O-Pins */
  /* LED Anzeige */
  for (int i = 0; i <= 12; i++){
    pinMode(LEDs[i], OUTPUT);
    digitalWrite(LEDs[i], LOW);
  };
 /* Bedinelemente und Kontrollleds */
  pinMode(statled, OUTPUT);
  pinMode(called, OUTPUT);
  pinMode(statbtn, INPUT);
  pinMode(calbtn, INPUT);

  /* Initialisierung des Seriellen Protokolls und des Rotationssensors */
  Serial.begin(31250);
  Wire.begin(sda, scl);
  if(!myMPU9250.init()){
    Serial.println("MPU9250 antwortet nicht / nicht verbunden");
  }
  else{
    Serial.println("MPU9250 erfolgreich verbunden");
  }
  /* Kalibrierung des Sensors auf 0 bei aktueller Position */
    Serial.println("Position you MPU9250 flat and don't move it - calibrating...");
    delay(1000);
    myMPU9250.autoOffsets();
    Serial.println("Done!");

  /*Samplerate von Gyroskop und Beschleunigungssensor: Sample rate = Internal sample rate / (1 + divider), Divider is a number 0...255, 0<DLPF<7 */
    myMPU9250.setSampleRateDivider(5); 
  /* Interval des Beschleunigungssensors: 2,4,8,16 G */
    myMPU9250.setAccRange(MPU9250_ACC_RANGE_2G);
  /* Low-Pass-Filter des BEschleunigungssensors */
    myMPU9250.enableAccDLPF(true);
  /*  Digital low pass filter (DLPF) for the accelerometer, if enabled  *  MPU9250_DPLF_0, MPU9250_DPLF_2, ...... MPU9250_DPLF_7 
  *   DLPF     Bandwidth [Hz]      Delay [ms]    Output rate [kHz]
  *     0           460               1.94           1
  *     1           184               5.80           1
  *     2            92               7.80           1
  *     3            41              11.80           1
  *     4            20              19.80           1
  *     5            10              35.70           1
  *     6             5              66.96           1
  *     7           460               1.94           1
  */
    myMPU9250.setAccDLPF(MPU9250_DLPF_6); 

  /* Bluetooth INI */
  SerialBT.begin("SynvOR - Rotationseingabegerät"); //Bluetooth device name
  Serial.println("Bereit für Bluetoothverbindung!");
  
}
 
void loop() {
  /* Lesen der Rotationswerte */
  float pitch = myMPU9250.getPitch();
  float roll  = myMPU9250.getRoll();

  if(digitalRead(statbtn) == LOW){
    digitalWrite(statled, HIGH);
    Serial.print("Pitch   = "); 
    Serial.print(pitch); 
    Serial.print("  |  Roll    = "); 
    Serial.println(roll); 
  
    Serial.println();
    SerialBT.print("Pitch = ");
    SerialBT.println(pitch);
    SerialBT.print("Roll = ");
    SerialBT.println(roll);
    digitalWrite(statled, HIGH);
    delay(100);
  }else if(digitalRead(statbtn) == HIGH){
    digitalWrite(statled, LOW);
    delay(100);
  }

  if(digitalRead(calbtn) == LOW){
    Serial.println("Position you MPU9250 flat and don't move it - calibrating...");
    delay(1000);
    myMPU9250.autoOffsets();
    Serial.println("Done!");
    Serial.println();
    delay(100);
  }else if(digitalRead(calbtn) == HIGH){
    digitalWrite(called, LOW);
    delay(100);
  }
  
  /* Bluetooth-Serielle Schnittstelle */
    if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    Serial.write(SerialBT.read());
  } 
  
}