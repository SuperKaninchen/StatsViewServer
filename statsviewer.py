import argparse
import rrdtool
import time
import wsgi
import stats_tracker


def initParser(parser):
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

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


def record():
    stats = stats_tracker.Stats()

    recording = True
    while recording:
        stats.update()
        rrd_string = stats.getRRDString()
        print(rrd_string)

        rrdtool.update(
            "statsviewer.rrd",
            rrd_string
        )
        time.sleep(1)



def serve():
    wsgi.main()      


def init():
    rrdtool.create(
        "statsviewer.rrd",
        "--step", "1",
        "DS:cpu_usage:GAUGE:30:0:100",
        "DS:mem_usage:GAUGE:30:0:100",
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
        record()
    
    elif args.command == "serve":
        serve()

    elif args.command == "init":
        init()


if __name__ == "__main__":
    main()