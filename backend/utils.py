
from typing import Callable, Tuple
import threading
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

def run_in_thread(func: Callable, *args, **kwargs) -> threading.Thread:
    """Run the given function in a new thread with parameters."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread