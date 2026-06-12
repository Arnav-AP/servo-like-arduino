from pyfirmata2 import Arduino

_active_board = None


class Board:
    def __init__(self, port):
        """Initialize and connect to Arduino board.

        Args:
            port: Serial port (e.g., '/dev/ttyUSB0' on Linux, 'COM3' on Windows)
        """
        global _active_board

        self.port = port
        self._board = Arduino(port)
        self._connected = True

        _active_board = self

    @staticmethod
    def get_active_board():
        """Get the currently active board instance."""
        global _active_board

        if _active_board is None:
            raise RuntimeError(
                "No board initialized. Create a Board first."
            )

        return _active_board

    def is_connected(self):
        """Check if board is still connected."""
        return self._connected

    def close(self):
        """Close the connection to the Arduino board."""
        if self._board:
            self._board.exit()
            self._connected = False
