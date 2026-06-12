from servo_like_arduino import *

board = Board('/dev/ttyUSB0')

# Multiple servos on different pins
servo1 = Servo()
servo1.attach(6)

servo2 = Servo()
servo2.attach(9)

# Servo with custom angle range (0-160 instead of 0-180)
servo3 = Servo()
servo3.attach(10, min_angle=0, max_angle=160)

# Check if servos are attached
if servo1.attached():
    print("Servo 1 is attached")

# Move all servos
servo1.write(0)
servo2.write(90)
servo3.write(80)

delay(500)

# Move them again
servo1.write(180)
servo2.write(45)
servo3.write(160)

delay(500)

# Detach when done
servo1.detach()
servo2.detach()
servo3.detach()

if board.is_connected():
    board.close()

