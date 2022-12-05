import psutil


class Stats(object):
    cpu_percent = 0
    mem_used = 0
    mem_total = 0
    total_times = {}
    diff_times = {}
    temps = {}

    def __init__(self) -> None:
        self.mem_total = psutil.virtual_memory().total
        self.total_times = psutil.cpu_times()._asdict()
        
        self.update()
    
    def _unpackTemps(self):
        temps = psutil.sensors_temperatures()["dell_smm"]
        for temp in temps:
            if temp.label in ["CPU", "SODIMM", "GPU", "Ambient"]:
                self.temps[temp.label] = temp.current


    def update(self):
        times = psutil.cpu_times()._asdict()
        for time in times:
            self.diff_times[time] = times[time]-self.total_times[time]
            self.total_times[time] = times[time]
        self.cpu_percent = int(psutil.cpu_percent(interval=None))
        self.mem_used = psutil.virtual_memory().used
        self.mem_percent = int(self.mem_used / self.mem_total * 100)

        self._unpackTemps()
    
    def getRRDString(self):
        out = "N:%s:%s:%s:%s:%s:%s" % (
            self.cpu_percent,
            self.mem_percent,
            self.temps["CPU"],
            self.temps["SODIMM"],
            self.temps["GPU"],
            self.temps["Ambient"]
        )
        return out