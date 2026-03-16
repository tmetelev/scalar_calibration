#include<Wire.h>

// Gyro
const int MPU = 0x68;
#define N 600*2
#define T 100


void sendAcc() {
  int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
  float Wz;
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 14, true);
  AcX = Wire.read() << 8 | Wire.read();
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();
  Tmp = Wire.read() << 8 | Wire.read();
  GyX = Wire.read() << 8 | Wire.read();
  GyY = Wire.read() << 8 | Wire.read();
  GyZ = Wire.read() << 8 | Wire.read();
  Serial.print(-AcX);
  Serial.print(" ");
  Serial.print(-AcY);
  Serial.print(" ");
  Serial.println(-AcZ);
}
void setup() {
  Serial.begin(9600);

  // Gyro
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}


void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'g') {
      Serial.println(N);
      for (int i = 0; i < N; i++) {
        sendAcc();
        delay(T);
      }
    }
  } else {
    delay(1000);
  }
//  sendAcc();
//  delay(2000);
}
