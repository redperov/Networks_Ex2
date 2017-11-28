import sys
from parser import *
from cache import Cache
from socket import socket, AF_INET, SOCK_DGRAM


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
source_ip, source_port = parse_ip_port(sys.argv[2])
root_ip, root_port = parse_ip_port(sys.argv[3])
file_path = sys.argv[4]

# Create a cache
cache = Cache()
cache.load_file(file_path)

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

s.bind((source_ip, source_port))
while True:
    request, sender_info = s.recvfrom(2048)
    print "Message: ", request, " from: ", sender_info
    answer = str(handle_request(request))
    s.sendto(answer, sender_info)
