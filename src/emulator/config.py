import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="UNIX shell emulator")
    parser.add_argument("--vfs", help="path to XML VFS")
    parser.add_argument("--script", help="path to startup script")
    parser.add_argument("--debug-config", action="store_true", help="print parsed configuration")
    return parser.parse_args()
