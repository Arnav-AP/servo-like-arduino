# servo-like-arduino

Arduino-style servo control for Python using PyFirmata2.

## Installation

```bash
pip install pyfirmata2
pip install servo-like-arduino
```

## Arduino Setup

Upload StandardFirmata to your Arduino:

File → Examples → Firmata → StandardFirmata

## Example

```python
from servo_like_arduino import *

Board('/dev/ttyUSB0')

servo = Servo()
servo.attach(9)

servo.write(0)
delay(1000)

servo.write(90)
delay(1000)

servo.write(180)
```

## Features

- Arduino-like syntax
- Simple servo control
- Built on PyFirmata2
- Compatible with StandardFirmata