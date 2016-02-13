import argparse


class ArgumentParserError(Exception):
    pass


class ThrowingParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message, self.format_help())
