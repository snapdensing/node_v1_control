import serial
ser = serial.Serial('/dev/ttyUSB0')
print(ser.name)

atcomPL = b'\x7e\x00\x04\x08\x01\x50\x4c\x5a'
ser.write(atcomPL)
line = ser.read(10)
print(line)

ser.close()
