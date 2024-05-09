import time
import serial

arduino=serial.Serial(port='COM4', baudrate=115200, timeout=0.1)


def send_message(val):
    encodedMessage=val.encode()
    arduino.write(encodedMessage)
    print(encodedMessage)    
    data=arduino.readlines()
    print (data)

time.sleep(3)

send_message("|i_13|")
send_message("|o_13|")

while(True):
    send_message("|s_D_13_1|")
    time.sleep(1)
    send_message("|s_D_13_0|")
    time.sleep(1)