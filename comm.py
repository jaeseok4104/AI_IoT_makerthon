import serial

ser = serial.Serial('/dev/ttyACM0', 115200)
y=ser.readable()
# print(y)
print('a')