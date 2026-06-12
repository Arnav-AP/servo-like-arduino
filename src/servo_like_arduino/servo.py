import servo_like_arduino.board as board_module


class Servo:
    def __init__(self):
        self._servo = None
        self.pin = None
        self.min_angle = 0
        self.max_angle = 180

    def attach(self, pin, min_angle=0, max_angle=180):
        """Attach servo to a pin with optional angle bounds.

        Args:
            pin: Digital pin number
            min_angle: Minimum angle (default 0)
            max_angle: Maximum angle (default 180)
        """
        board = board_module.Board.get_active_board()

        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._servo = board._board.get_pin(f"d:{pin}:s")

    def write(self, angle):
        """Write angle to servo.

        Args:
            angle: Angle in degrees (will be clamped to min/max bounds)
        """
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        if angle < self.min_angle:
            angle = self.min_angle

        if angle > self.max_angle:
            angle = self.max_angle

        self._servo.write(angle)

    def writeMicroseconds(self, us):
        """Write microseconds to servo (1000-2000 typical range).

        Args:
            us: Microseconds value
        """
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        self._servo.write(us)

    def read(self):
        """Read current servo angle."""
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        return self._servo.read()

    def attached(self):
        """Check if servo is attached."""
        return self._servo is not None

    def detach(self):
        """Detach servo and release the pin."""
        if self._servo is not None:
            self._servo.disable()
            self._servo = None
            self.pin = None
