import sys
from cache import Cache
from parser_commands import *
from socket import socket, AF_INET, SOCK_DGRAM


def local_search(client_request):
    """
    Looks in the cache for the answer to the client's request.
    :param client_request: string in format [domain] [type]
    :return: record
    """
    # Split request to fields.
    domain, request_type = parse_request(client_request)

    # Search for the record in the cache.
    record = cache.check_record(domain, request_type)

    return record


def save_record(str_record):
    """
    Saves the new record in the cache.
    :param str_record: string record
    :return: None
    """
    record = parse_to_record(str_record)
    cache.add_record(record)


# Get command line arguments.
# The format: [resolver_ip:resolver:port]
dest_ip, dest_port = parse_ip_port(sys.argv[1])

# Create a cache.
cache = Cache()

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

msg = raw_input("Message to send: ")
while not msg == 'quit':

    # Look for an answer in the cache.
    local_answer = local_search(msg)

    # If answer was found in the cache.
    if local_answer:
        print "Local answer:\n", str(local_answer)

    else:  # If no answer was found in the cache, ask the resolver server.
        # Perform a request to the server.
        s.sendto(msg, (dest_ip, dest_port))
        response, _ = s.recvfrom(2048)
        print "Server sent:\n", response

        if response != "Don't know":
            # Save the answer in the cache.
            save_record(response)

    msg = raw_input("Message to send: ")

s.close()
