import shlex


class ParseError(ValueError):
    """Raised when a command line cannot be parsed."""


def parse_command(line):
    try:
        return shlex.split(line)
    except ValueError as exc:
        raise ParseError(str(exc)) from exc
