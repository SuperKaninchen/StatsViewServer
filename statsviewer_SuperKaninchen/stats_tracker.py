import psutil


class Stats(object):
    cpu_percent = 0
    mem_used = 0
    mem_total = 0
    total_times = {}
    diff_times = {}

    def __init__(self) -> None:
        self.mem_total = psutil.virtual_memory().total
        self.total_times = psutil.cpu_times()._asdict()
        self.update()

    def update(self):
        times = psutil.cpu_times()._asdict()
        for time in times:
            self.diff_times[time] = times[time]-self.total_times[time]
            self.total_times[time] = times[time]
        self.cpu_percent = int(psutil.cpu_percent(interval=None))
        self.mem_used = psutil.virtual_memory().used
        self.mem_percent = int(self.mem_used / self.mem_total * 100)
    
    def getRRDString(self):
        out = "N:" + str(self.cpu_percent) + ":" + str(self.mem_percent)
        return out