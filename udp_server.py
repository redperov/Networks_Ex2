import sys
from cache import Cache
from socket import socket, AF_INET, SOCK_DGRAM


def parse_is_resolver(str_input):
    """
    Parses the is resolver answer from string to boolean.
    :param str_answer: is resolver string
    :return: boolean
    """
    if str_input == "y":
        return True
    else:
        return False


def parse_ip_port(str_input):
    """
    Parses the ip and port from string to separate values
    :param str_input: string input
    :return: [ip, port]
    """
    ip = str_input.split(':')[0]
    port = int(str_input.split(':')[1])

    return ip, port


def handle_request(request):
    """
    Handles the client's request.
    :param request: request in format: [domain] [type]
    :return: record
    """
    name, request_type = request.split()
    # check if the answer exists in the cache.
    record = cache.check_record(name, request_type)
    if record is not None:
        return record
    elif is_resolver:
        pass  # TODO implement
    else:
        pass  # TODO implement


# Get command line arguments.
# The format: [is_resolver] [ip:port] [root_ip:root_port] [mappings_path]
is_resolver = parse_is_resolver(sys.argv[1])
my_ip, my_port = parse_ip_port(sys.argv[2])
root_ip, root_port = parse_ip_port(sys.argv[3])
file_path = sys.argv[4]

# Create a cache
cache = Cache()
cache.load_file(file_path)

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

source_ip = '127.0.0.1'
source_port = 12345
s.bind((source_ip, source_port))
while True:
    request, sender_info = s.recvfrom(2048)
    print "Message: ", request, " from: ", sender_info
    answer = str(handle_request(request))
    s.sendto(answer, sender_info)
