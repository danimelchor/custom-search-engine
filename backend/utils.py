
from typing import Callable, Tuple
import threading
import optparse


def parse_args() -> str:
    """Parse the command line arguments."""
    parser = optparse.OptionParser()

    # Query argument
    parser.add_option('-q', '--query', action="store", dest="query", help="query string", default="")

    options, _ = parser.parse_args()

    return options.query