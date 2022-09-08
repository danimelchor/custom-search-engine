
from typing import Tuple
import optparse


def parse_args() -> Tuple[str, int]:
    """Parse the command line arguments."""
    parser = optparse.OptionParser()

    # host option
    parser.add_option('-H', '--host',
                      action="store", dest="host",
                      help="host string", default="localhost")
    # port option
    parser.add_option('-p', '--port',
                      action="store", dest="port",
                      help="port int", default="5000")

    options, _ = parser.parse_args()

    print(options.host, options.port)
    return (options.host, int(options.port))