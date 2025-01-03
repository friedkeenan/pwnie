from .proxies import LoggingProxy

import argparse

def run_proxy(args):
    class Proxy(LoggingProxy):
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

main(parser.parse_args())
