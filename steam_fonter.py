import argparse
import re
import sys


parser = argparse.ArgumentParser()

parser.add_argument(
    'increase',
    type=float,
)

parser.add_argument(
    'infile',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin,
)

parser.add_argument(
    'outfile',
    nargs='?',
    type=argparse.FileType('w'),
    default=sys.stdout,
)

FONT_RE = re.compile(r'font-size=(?P<quote>"?)(?P<size>\d+)(?P=quote)')


def main():
    args = parser.parse_args()

    def processor(matchobj):
        return 'font-size={quote}{size:d}{quote}'.format(
            quote=matchobj.group('quote'),
            size=int(round(
                args.increase * int(matchobj.group('size'), 10)
            )),
        )

    with args.infile, args.outfile:
        for line in args.infile:
            line = FONT_RE.sub(repl=processor, string=line)
            args.outfile.write(line)


if __name__ == '__main__':
    main()
