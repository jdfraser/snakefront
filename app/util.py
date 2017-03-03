import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

class TimerPrint(Timer):
    def __init__(self, msg="Timer"):
        self.msg = msg
    def __exit__(self, *args):
        Timer.__exit__(self)
        print self.msg + ":", str(round(self.interval * 1000, 3)) + "ms"
