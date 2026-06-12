import servo_like_arduino.board as board_module


class Servo:
    def __init__(self):
        self._servo = None
        self.pin = None

    def attach(self, pin):
        board = board_module.Board.get_active_board()

        self.pin = pin
        self._servo = board._board.get_pin(f"d:{pin}:s")

    def write(self, angle):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        if angle < 0:
            angle = 0

        if angle > 180:
            angle = 180

        self._servo.write(angle)

    def read(self):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        return self._servo.read()