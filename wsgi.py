from flask import Flask, render_template, request
from stats_tracker import Stats
import graph_generator
import rrdtool

stats = Stats()
app = Flask(__name__)
timeframe = 60


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
    global timeframe
    if request.method == "POST":
        timeframe = int(request.form.get("timeframe"))

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
        "statsviewer.rrd",
        "LAST"
    )

    cpu_data = []
    mem_data = []

    for entry in result[2]:
        cpu_data.append(entry[0])
        mem_data.append(entry[1])


    cpu_graph = graph_generator.Graph(cpu_data, 1000, 250, 100, "Percent")
    mem_graph = graph_generator.Graph(
        mem_data, 1000, 250,
        stats.mem_total/(1024**2), "megaBytes")
    return [cpu_graph, mem_graph]
    

def main():
    stats.update()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()