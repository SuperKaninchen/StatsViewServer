from flask import Flask, render_template, request
from .stats_tracker import Stats
from .graph_generator import Graph
import rrdtool

stats = Stats()
app = Flask(__name__)
timeframe = 60
viewselect = "cpu_mem"
rrd_path = ""


def makeStatsDict(stats):
    cur_stats = {}
    cur_stats["cpu_percent"] = stats.cpu_percent
    cur_stats["mem_total"] = stats.mem_total / (1024 ** 2)
    cur_stats["mem_used"] = stats.mem_used / (1024 ** 2)
    cur_stats["mem_free"] = (stats.mem_total - stats.mem_used) / (1024 ** 2)
    cur_stats["mem_unit"] = "mB"
    return cur_stats


@app.route("/viewStats", methods=["GET", "POST"])
def viewStats():
    global timeframe, viewselect
    if request.method == "POST":
        timeframe = int(request.form.get("timeframe"))
        viewselect = request.form.get("viewselect")

    graphs = fetchGraphsFromRRD(timeframe)
    stats.update()
    stats_dict = makeStatsDict(stats)
    return render_template(
        "viewPageTemplate.jinja",
        cpu_percent = stats_dict["cpu_percent"],
        mem_total = stats_dict["mem_total"],
        mem_used = stats_dict["mem_used"],
        mem_free = stats_dict["mem_free"],
        mem_unit = stats_dict["mem_unit"],
        graphs = graphs,
        total_times = stats.total_times,
        diff_times = stats.diff_times
    )


def fetchGraphsFromRRD(timeframe):
    resolution = int(timeframe/100)+1
    print(resolution)
    result = rrdtool.fetch(
        "--start", "-"+str(timeframe),
        "--resolution", str(resolution),
        rrd_path,
        "LAST"
    )

    if viewselect == "cpu_mem":
        cpu_data = []
        mem_data = []

        for entry in result[2]:
            cpu_data.append(entry[0])
            mem_data.append(entry[1])

        cpu_graph = Graph("CPU usage", cpu_data, 1000, 250, 100, "Percent")
        mem_graph = Graph(
            "RAM usage",
            mem_data, 1000, 250,
            int(stats.mem_total/(1024**2)), "megaBytes")
        
        graphs = [cpu_graph, mem_graph]
    
    elif viewselect == "temps":
        cpu_data = []
        sodimm_data = []
        gpu_data = []
        ambient_data = []

        for entry in result[2]:
            cpu_data.append(entry[2])
            sodimm_data.append(entry[3])
            gpu_data.append(entry[4])
            ambient_data.append(entry[5])
        
        cpu_graph = Graph("CPU temperature", cpu_data, 1000, 250, 100, "Degrees")
        sodimm_graph = Graph("SODIMM temperature", sodimm_data, 1000, 250, 100, "Degrees")
        gpu_graph = Graph("GPU temperature", gpu_data, 1000, 250, 100, "Degrees")
        ambient_graph = Graph("Ambient temperature", ambient_data, 1000, 250, 100, "Degrees")
        
        graphs = [cpu_graph, sodimm_graph, gpu_graph, ambient_graph]

    return graphs
    

def runFlask(path):
    global rrd_path
    rrd_path = path
    stats.update()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    runFlask()