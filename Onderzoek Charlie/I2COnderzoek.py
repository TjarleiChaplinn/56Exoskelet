import time
import smbus

bus = smbus.SMBus(1)
address = 0x09

current_milli_time = lambda: int(round(time.time()*1000))

time.sleep(3)

def utf8len(s):
    return len(s.encode('utf-8'))

def writeString(value):
    for character in str(value):
        bus.write_byte(address, ord(character))
    return -1

def readString(value):
    byte_list = []
    for i in range(0,value):
        byte_list.append(bus.read_byte(address))
    result = "".join([chr(byte) for byte in byte_list])
    return result

for j in range(0,4):
    total_time = 0
    if j == 0:
        word = ('a' * 5)
    else:
        word = ('a' * j) * 10
    for i in range(0,10):
        send_time = current_milli_time()
        writeString(word)
        read_val = readString(utf8len(word))
        receive_time = current_milli_time()
        total_time += receive_time - send_time
    print("Hoeveelheid bytes: %s | Tijd: %s" % (utf8len(word), (total_time/10)))
