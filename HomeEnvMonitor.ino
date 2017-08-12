#include "DHT.h"
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

#define PT_USE_TIMER
#include "pt.h"

#define DHTPIN 11     // what digital pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

static struct pt thread_dht, thread_g5s, thread_pi;

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
SoftwareSerial Serial_g5s(3, 2);

float currentH = 0.0;
float currentT = 0.0;
int currentPM2_5 = 0;
int currentPM10 = 0;
int currentF = 0;

void setup() {
  Serial.begin(9600);
  Serial_g5s.begin(9600);
  lcd.begin(16, 2);
  dht.begin();

  PT_INIT(&thread_dht);
  PT_INIT(&thread_g5s);
  PT_INIT(&thread_pi);
}

static int thread_dht_entry(struct pt *pt) {
  PT_BEGIN(pt);
  while (1) {
    currentH = dht.readHumidity();
    currentT = dht.readTemperature();

    lcd.setCursor(0, 0);
    lcd.print("H:");
    lcd.print(currentH);
    lcd.print(" T:");
    lcd.print(currentT);
    PT_TIMER_DELAY(pt, 200);
  }
  PT_END(pt);
}

static int thread_g5s_entry(struct pt *pt) {
  PT_BEGIN(pt);
  while (1) {
    uint8_t mData = 0;
    uint8_t mPkt[32] = {0};
    int mCheck = 0;

    while (Serial_g5s.available() > 0) {
      mData = Serial_g5s.read();
      delay(2);//wait until packet is received
      if (mData == 0x42) {
        mPkt[0] =  mData;
        mData = Serial_g5s.read();
        if (mData == 0x4d) {
          mPkt[1] =  mData;
          mCheck = 66 + 77;
          for (int i = 2; i < 30; i++) {
            mPkt[i] = Serial_g5s.read();
            delay(2);
            mCheck += mPkt[i];
          }
          mPkt[30] = Serial_g5s.read();
          delay(1);
          mPkt[31] = Serial_g5s.read();

          if (mCheck == mPkt[30] * 256 + mPkt[31]) {
            currentPM2_5 = mPkt[12] * 256 + mPkt[13];
            currentPM10 = mPkt[14] * 256 + mPkt[15];
            currentF = mPkt[28] * 256 + mPkt[29];

            lcd.setCursor(0, 1);
            lcd.print("P2:");
            lcd.print(currentPM2_5);
            lcd.print(" F:");
            lcd.print(currentF);
            lcd.print("    ");
          }
        }
      }
    }
    PT_TIMER_DELAY(pt, 200);
  }
  PT_END(pt);
}

unsigned long interval = 2000;
unsigned long record_time = 0;

static int thread_pi_entry(struct pt *pt) {
  PT_BEGIN(pt);
  while (1) {
    unsigned long nowtime = millis();
    if (nowtime > record_time + interval) {
      Serial.println("#");
      Serial.println(currentH);
      Serial.println(currentT);
      Serial.println(currentPM2_5);
      Serial.println(currentPM10);
      Serial.println(currentF);
      Serial.println("*");
      record_time = nowtime;
    }
    PT_TIMER_DELAY(pt, 200);
  }
  PT_END(pt);
}

void loop() {
  thread_dht_entry(&thread_dht);
  thread_g5s_entry(&thread_g5s);
  thread_pi_entry(&thread_pi);
}
