import argparse
import colorama

from .monitor import Monitor

parser = argparse.ArgumentParser(
    prog="pymon",
)

parser.add_argument(
    "filename",
    type=str,
    help="the file to be executed with pymon",
    metavar="filename",
)

parser.add_argument(
    "-p",
    "--patterns",
    type=str,
    help='the file patterns to monitor. use once for each pattern. default "*.py"',
    action="append",
    default=["*.py"],
    metavar="patterns",
)

parser.add_argument(
    "-w",
    "--watch",
    type=str,
    help='the directory to monitor for changes. default "."',
    action="store",
    default=".",
    metavar="path",
)

parser.add_argument(
    "-a",
    "--args",
    type=str,
    help="arguments to pass on to the execution script",
    action="store",
    default=[],
    metavar="command",
)


def main():
    colorama.init()
    arguments = parser.parse_args()

    monitor = Monitor(arguments)
    monitor.start()

    try:
        while True:
            pass
            # cmd = input()
            # if cmd == "rs":
            #     monitor.restart_process()
            # elif cmd == "stop":
            #     monitor.stop()
            #     break
    except KeyboardInterrupt:
        monitor.stop()

    return


if __name__ == "__main__":
    main()
