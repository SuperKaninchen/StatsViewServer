from flask import Flask, render_template
from stats_tracker import Stats

stats = Stats()
app = Flask(__name__)


def makeStatsDict(stats):
    cur_stats = {}
    cur_stats["cpu_percent"] = stats.cpu_percent
    cur_stats["mem_total"] = stats.mem_total / (1024 ** 2)
    cur_stats["mem_used"] = stats.mem_used / (1024 ** 2)
    cur_stats["mem_free"] = (stats.mem_total - stats.mem_used) / (1024 ** 2)
    cur_stats["mem_unit"] = "mB"
    return cur_stats


@app.route("/viewStats")
def viewStats():
    stats.update()
    stats_dict = makeStatsDict(stats)
    return render_template(
        "viewPageTemplate.html",
        cpu_percent = stats_dict["cpu_percent"],
        mem_total = stats_dict["mem_total"],
        mem_used = stats_dict["mem_used"],
        mem_free = stats_dict["mem_free"],
        mem_unit = stats_dict["mem_unit"]
    )


def main():
    stats.update()
    app.run()


if __name__ == "__main__":
    main()