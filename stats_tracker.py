import psutil


class Stats(object):
    cpu_percent = 0
    mem_used = 0
    mem_total = 0

    def __init__(self) -> None:
        self.mem_total = psutil.virtual_memory().total
        self.update()

    def update(self):
        self.cpu_percent = psutil.cpu_percent(interval=None)
        self.mem_used = psutil.virtual_memory().used