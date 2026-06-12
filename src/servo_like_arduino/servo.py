import servo_like_arduino.board as board_module
from .utils import delay


class Servo:
    def __init__(self):
        self._servo = None
        self.pin = None
        self.min_angle = 0
        self.max_angle = 180
        self.current_angle = None

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

    def detach(self):
        """Detach servo and release the pin."""
        if self._servo is not None:
            self._servo.disable()
            self._servo = None
            self.pin = None
            self.current_angle = None

    def write(self, angle):
        """Write angle to servo.

        Args:
            angle: Angle in degrees (will be clamped to min/max bounds)
        """
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        try:
            angle = int(angle)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"angle must be a number between {self.min_angle} and {self.max_angle}") from exc

        angle = max(self.min_angle, min(self.max_angle, angle))

        self._servo.write(angle)
        self.current_angle = angle

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

        if self.current_angle is None:
            raise RuntimeError(
                "Servo angle is unknown. Call write() first."
            )

        return self.current_angle

    def attached(self):
        """Check if servo is attached."""
        return self._servo is not None

    def move_smooth(self, target_angle, delay_ms=15):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        try:
            target_angle = int(target_angle)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"target_angle must be a number between {self.min_angle} and {self.max_angle}") from exc

        target_angle = max(self.min_angle, min(self.max_angle, target_angle))

        if self.current_angle is None:
            self.write(target_angle)
            return

        if target_angle == self.current_angle:
            return

        step = 1 if target_angle > self.current_angle else -1

        for angle in range(
            self.current_angle + step,
            target_angle + step,
            step
        ):
            self.write(angle)
            delay(delay_ms)

    def sweep(
        self,
        start=0,
        end=180,
        step=1,
        delay_ms=15
    ):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        if step <= 0:
            raise ValueError(
                "step must be greater than 0"
            )

        try:
            start = int(start)
            end = int(end)
        except (TypeError, ValueError) as exc:
            raise ValueError("start and end must be numbers") from exc

        start = max(self.min_angle, min(self.max_angle, start))
        end = max(self.min_angle, min(self.max_angle, end))

        if start < end:
            for angle in range(start, end + 1, step):
                self.write(angle)
                delay(delay_ms)
        else:
            for angle in range(start, end - 1, -step):
                self.write(angle)
                delay(delay_ms)
