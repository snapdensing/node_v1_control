import argparse

# Parser
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--srclog", help="source logfile")

args = parser.parser_args()

## Default source log file
if args.srclog:
  srclog = args.srclog
else:
  srclog = '/var/log/aggregator.log'


