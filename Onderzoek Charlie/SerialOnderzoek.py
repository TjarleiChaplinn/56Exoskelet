import time
import serial

current_milli_time = lambda: int(round(time.time()*1000))

def utf8len(s):
    return len(s.encode('utf-8'))

ser = serial.Serial('/dev/ttyUSB0',9600)
time.sleep(3)
print(ser.name)
for j in range(0,4):
    total_time = 0
    if j == 0:
        word = ('a' * 5)
    else:
        word = ('a' * j) * 10
    for i in range(0,10):
        send_time = current_milli_time()
        ser.write(str(word).encode('utf-8'))
        read_val = ser.read(size=utf8len(word))
        receive_time = current_milli_time()
        total_time += receive_time - send_time
    print("Hoeveelheid bytes: %s | Tijd: %s" % (utf8len(word), (total_time/10)))

ser.close()