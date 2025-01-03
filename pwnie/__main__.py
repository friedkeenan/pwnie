from .proxies import (
    LoggingProxy,
    FlyProxy,
)

import argparse

def run_proxy(args):
    class Proxy(LoggingProxy, *args.cheats):
        LOG_NOISY_PACKETS = not args.quiet

    print("Proxying...")

    Proxy().run()

def main(args):
    if args.action == "proxy":
        run_proxy(args)

parser = argparse.ArgumentParser(prog="caseus")

subparsers = parser.add_subparsers()

proxy_parser = subparsers.add_parser("proxy")
proxy_parser.set_defaults(action="proxy")

proxy_parser.add_argument("-q", "--quiet", help="Disables logging noisier packets", action="store_true")

proxy_parser.add_argument(
    "--fly", help="Allows players to fly",

    action = "append_const",
    dest   = "cheats",
    const  = FlyProxy,
)

main(parser.parse_args())
