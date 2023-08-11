import argparse
import rrdtool
import time
from .wsgi import runFlask
from .stats_tracker import Stats

rrd_tasks = []

def initParser(parser):
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    parser.add_argument(
        "path",
        help="path to the Round-Robin Database file (.rrd)"
    )

    record_parser = subparsers.add_parser(
        "record",
        help="record machine stats to RRD"
    )

    record_parser = subparsers.add_parser(
        "serve",
        help="Start flask server"
    )

    init_parser = subparsers.add_parser(
        "init",
        help="init the RRD"
    )


def record(path):
    stats = Stats()

    recording = True
    while recording:
        stats.update()
        rrd_string = stats.getRRDString()

        rrdtool.update(
            path,
            rrd_string
        )
        time.sleep(1)



def serve(path):
    runFlask(path)


def init(path):
    stats = Stats()
    rrdtool.create(
        path,
        "--step", "1",
        "DS:cpu_usage:GAUGE:30:0:100",
        "DS:mem_usage:GAUGE:30:0:"+str(stats.mem_total/1000000),
        "DS:cpu_temp:GAUGE:30:0:200",
        "DS:sodimm_temp:GAUGE:30:0:200",
        "DS:gpu_temp:GAUGE:30:0:200",
        "DS:ambient_temp:GAUGE:30:0:200",
        "RRA:AVERAGE:0.5:1s:1m",  # for displaying every second of one minute
        "RRA:AVERAGE:0.5:6s:10m",  # for displaying 100 6-second segments of 10 minutes
        "RRA:AVERAGE:0.5:36s:1h",  # for displaying 100 36-second segments of 1 hour
        "RRA:AVERAGE:0.5:864s:1d",  # for displaying 100 864-second segments of 1 day
        "RRA:AVERAGE:0.5:1:864000",
        "RRA:AVERAGE:0.5:60:129600",
        "RRA:AVERAGE:0.5:3600:13392",
        "RRA:AVERAGE:0.5:86400:3660"
    )


def main():
    parser = argparse.ArgumentParser(
        prog="Stats Viewer",
        description="Saves machine stats to RRD and views it as graphs using flask"
    )
    initParser(parser)
    args = parser.parse_args()

    if args.command == "record":
        record(args.path)

    elif args.command == "serve":
        serve(args.path)

    elif args.command == "init":
        init(args.path)


if __name__ == "__main__":
    main()