import serial
import time

arduino = None
try:
  port = '/dev/tty.usbmodem1411'
  arduino = serial.Serial(port, 9600)
  time.sleep(1)
except Exception:
  pass


def sendByteToArduino(data):
  if arduino:
    arduino.write(data)


def testArduino():
  arduino.write(b'1')
  msg = arduino.readline()
  print(msg)


if __name__ == '__main__':
  while(True):
    testArduino()
