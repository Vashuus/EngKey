"""Debouncer con Timer — útil para retrasar una acción hasta que
el usuario deje de escribir."""

import threading


class Debouncer:
    """Ejecuta *fn* tras *delay_ms* de silencio.
    Cada llamada a .poke() reinicia el contador.
    """

    def __init__(self, delay_ms: int, fn):
        self._delay = delay_ms / 1000
        self._fn = fn
        self._timer: threading.Timer | None = None

    def poke(self):
        self.cancel()
        self._timer = threading.Timer(self._delay, self._fn)
        self._timer.daemon = True
        self._timer.start()

    def cancel(self):
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None
