"""Lightweight logging with timestamps and file output."""

from pybricks.tools import StopWatch  # pyright: ignore[reportMissingImports]

LOG_FILE = "run_log.txt"
_timer = StopWatch()
_timer.reset()


def set_log_file(path):
    global LOG_FILE
    LOG_FILE = path


def _timestamp(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    millis = ms % 1000
    return "[{:02d}:{:02d}.{:03d}]".format(int(minutes), int(seconds), int(millis))


def log(message):
    if message is None:
        return
    ms = _timer.time()
    text = "{} {}".format(_timestamp(ms), message)
    print(text)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(text + "\n")
    except Exception:
        pass
