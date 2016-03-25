import argparse


class ArgumentParseException(Exception):
    pass


class ThrowingParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParseException(message, self.format_help())
