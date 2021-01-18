import time
import can

current_milli_time = lambda: int(round(time.time()*1000))

time.sleep(3)

def utf8len(s):
    return len(s.encode('utf-8'))

try:
    bus = can.interface.Bus(bustype='serial', channel='/dev/ttyAMA0',bitrate=9600)
except OSError:
    print('Cannot find port')
    exit()

def sendString(value):
    n = 8
    temp = [value[i:i+n] for i in range(0, len(value), n)]
    for tempStr in temp:
        msg = can.Message(data=tempStr)
        try:
            bus.send(msg)
        except can.CanError:
            print("Message not sent!")

def readString(value):
    tempStr = ""
    while True:
        temp = bus.recv()
        tempStr.append(temp)
        value -= 8
        if value <= 0:
            break
    return tempStr

for j in range(0,4):
    total_time = 0
    if j == 0:
        word = ('a' * 5)
    else:
        word = ('a' * j) * 10
    for i in range(0,10):
        send_time = current_milli_time()
        sendString(word)
        read_val = readString(utf8len(word))
        receive_time = current_milli_time()
        total_time += receive_time - send_time
    print("Hoeveelheid bytes: %s | Tijd: %s" % (utf8len(word), (total_time/10)))    
