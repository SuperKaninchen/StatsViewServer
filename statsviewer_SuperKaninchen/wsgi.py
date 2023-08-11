from flask import Flask, render_template, request, redirect
from .stats_tracker import Stats
from .graph_generator import Graph
import rrdtool
import time

stats = Stats()
app = Flask(__name__)

timeframe = 60
viewselect = "cpu_mem"
resolution = 100

rrd_path = ""


@app.route("/")
def viewIndex():
    return redirect("viewStats")

@app.route("/viewStats", methods=["GET", "POST"])
def viewStats():
    global timeframe, viewselect, resolution
    if request.method == "POST":
        timeframe = int(request.form.get("timeframe"))
        viewselect = request.form.get("viewselect")
        resolution = int(request.form.get("resolution"))
        return redirect("viewStats")
    else:
        if not timeframe:
            timeframe = 60
        if not viewselect:
            viewselect = "cpu_mem"
        if not resolution:
            resolution = 100

        graphs = fetchGraphsFromRRD(timeframe)
        tables = fetchTablesFromTracker()
        stats.update()
        return render_template(
            "viewPageTemplate.jinja",
            timeframe = timeframe,
            viewselect = viewselect,
            resolution = resolution,
            graphs = graphs,
            tables = tables
        )


def fetchGraphsFromRRD(timeframe):
    result = rrdtool.fetch(
        "--start", "-"+str(timeframe),
        rrd_path,
        "LAST"
    )

    if viewselect == "cpu_mem":
        cpu_data = []
        mem_data = []

        for entry in result[2]:
            cpu_data.append(entry[0])
            mem_data.append(entry[1])

        cpu_graph = Graph("CPU usage", cpu_data, 1000, 250, 100, "Percent", resolution)
        mem_graph = Graph(
            "RAM usage",
            mem_data, 1000, 250,
            int(stats.mem_total/(1024**2)), "megaBytes", resolution)

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

        cpu_graph = Graph("CPU temperature", cpu_data, 1000, 250, 100, "Degrees", resolution)
        sodimm_graph = Graph("SODIMM temperature", sodimm_data, 1000, 250, 100, "Degrees", resolution)
        gpu_graph = Graph("GPU temperature", gpu_data, 1000, 250, 100, "Degrees", resolution)
        ambient_graph = Graph("Ambient temperature", ambient_data, 1000, 250, 100, "Degrees", resolution)

        graphs = [cpu_graph, sodimm_graph, gpu_graph, ambient_graph]

    return graphs


def fetchTablesFromTracker():
    tables = []

    tables.append({
        "title": "Total CPU times",
        "unit": "seconds",
        "entries": stats.total_times
    })
    tables.append({
        "title": "CPU times since last update",
        "unit": "seconds",
        "entries": stats.diff_times
    })

    temps = stats.temps
    for temp_source in temps:
        tables.append({
            "title": "Temperature Sensor " + temp_source,
            "unit": "degrees Celsius",
            "entries": temps[temp_source]
        })

    return tables




def runFlask(path):
    global rrd_path
    rrd_path = path
    stats.update()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    runFlask()