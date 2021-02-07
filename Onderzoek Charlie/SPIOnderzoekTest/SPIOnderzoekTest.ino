#include <SPI.h>

volatile byte Slavereceived,Slavesend;

void setup() {
  Serial.begin(115200);
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
}

void loop() {
}

ISR (SPI_STC_vect){
  Slavereceived = SPDR;
  Slavesend = Slavereceived;
  SPDR = Slavesend;
}
