import spidev
import time

current_milli_time = lambda: int(round(time.time()*1000))

def utf8len(s):
    return len(s.encode('utf-8'))

time.sleep(3)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 5000

for j in range(0,4):
    total_time = 0
    if j == 0:
        word = ('a' * 5)
    else:
        word = ('a' * j) * 10
    for i in range(0,10):
        send_time = current_milli_time()
        read_val = spi.xfer(bytes(str(word).encode('utf-8')))
        receive_time = current_milli_time()
        total_time += receive_time - send_time
    print("Hoeveelheid bytes: %s | Tijd: %s" % (utf8len(word), (total_time/10)))