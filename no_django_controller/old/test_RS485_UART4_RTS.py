import time, struct, fcntl, serial
uart4_file = '/dev/ttyO4'
baud = 19200
ser = serial.Serial(uart4_file, baud)
fd=ser.fileno()
serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
fcntl.ioctl(fd,0x542F,serial_rs485)
while True:
    ser.write("Testing")
    print("I just wrote (without error) to the serial %s" % ser)
    time.sleep(1)