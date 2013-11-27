__author__ = 'jenkins'

import logging
import sys
import argparse

class BaseTool:

    def parse_args(self):
        args = self.parser.parse_args()
        level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(name)s:%(message)s', level=level, stream=sys.stderr)
        return args


    def main(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-d", "--debug", help="Print debug info",action='store_true')

        self.run(self.parser)

    def run(self, parser):
        raise Exception("Override this method!")





