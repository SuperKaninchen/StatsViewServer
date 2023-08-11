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
        temps = psutil.sensors_temperatures()
        for temp_source in temps:
            if temp_source and temps[temp_source]:
                self.temps[temp_source] = {}
                for temp in temps[temp_source]:
                    self.temps[temp_source][temp.label] = temp.current


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
        rrd_temps = {
            "CPU": -1,
            "SODIMM": -1,
            "GPU": -1,
            "Ambient": -1
        }
        for temp_source in self.temps:
            if temp_source in ["acpitz", "nvme", "coretemp"]:
                if temp_source == "coretemp":
                    print(self.temps[temp_source])
                    if "Package id 0" in self.temps[temp_source]:
                        rrd_temps["CPU"] = self.temps[temp_source]["Package id 0"]

            if "CPU" in self.temps[temp_source]:
                rrd_temps["CPU"] = self.temps[temp_source]["CPU"]
            if "SODIMM" in self.temps[temp_source]:
                rrd_temps["SODIMM"] = self.temps[temp_source]["SODIMM"]
            if "GPU" in self.temps[temp_source]:
                rrd_temps["GPU"] = self.temps[temp_source]["GPU"]
            if "Ambient" in self.temps[temp_source]:
                rrd_temps["Ambient"] = self.temps[temp_source]["Ambient"]

        out = "N:%s:%s:%s:%s:%s:%s" % (
            self.cpu_percent,
            self.mem_used/1000000,
            rrd_temps["CPU"],
            rrd_temps["SODIMM"],
            rrd_temps["GPU"],
            rrd_temps["Ambient"]
        )
        return out