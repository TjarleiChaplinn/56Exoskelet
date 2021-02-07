#include <Serial_CAN_Module.h>
#include <SoftwareSerial.h>

Serial_CAN can;

#define can_tx  2
#define can_rx  3

void setup()
{
    Serial.begin(9600);
    can.begin(can_tx, can_rx, 9600);      // tx, rx
    Serial.println("begin");
}

unsigned long id = 0;
unsigned char data[8];

void loop()
{
    if(can.recv(&id, dta))
    {
        can.send(0x55, 0, 0, 8, data);
    }
}
