#!/usr/bin/python
import os
import logging
import argparse


def get_cmd_line_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s -b [base_file] -a [addition1] [addition2] ...",
        description="Merger for russian tax software files"
    )
    parser.add_argument('-b', '--base', required=True, metavar="base_file.dc1",
                        help="Name of base file where to append data")
    parser.add_argument('-a', '--add', required=True, nargs='+', metavar="additional_file.dc1",
                        help="Name of file(s) to merge into base file")
    return parser.parse_args()


def main():
    LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
    logging.basicConfig(level=LOGLEVEL)

    args = get_cmd_line_args()
    print(f"B: {args.base}")
    print(f"A: {args.add}")


if __name__ == '__main__':
    main()