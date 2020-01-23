#include <Wire.h>
#include <stdbool.h>
#define MPU 0x68
volatile int16_t AcX,AcY,AcZ;
void UART_set() {
  Serial.begin(115200);
}

void MPU6050_set() {
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6b);
  Wire.write(0);
  Wire.endTransmission(true);

}

void update_data() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);

  AcX=Wire.read()<<8|Wire.read();   
  AcY=Wire.read()<<8|Wire.read(); 
  AcZ=Wire.read()<<8|Wire.read();
}
void post_data(){
  Serial.print(AcX);
  Serial.print("/");
  Serial.print(AcY);
  Serial.print("/");
  Serial.println(AcZ);
 
}

void setup() {
  UART_set();
  MPU6050_set();
}

void loop() {
  update_data();
  delay(30);
  post_data();
  delay(3);
  
}
