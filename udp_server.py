import sys
from dns import DnsRequest, DnsResponse
from parser_commands import *
from cache import Cache
from socket import socket, AF_INET, SOCK_DGRAM


def ns_search(domain):
    """
    Checks the cache to find the closest existing NS domain.
    :param domain: original domain
    :return: NS record, boolean is it the final answer.
    """

    # Try searching the original domain.
    record = cache.check_record(domain, "NS")

    if record is not None:
        return record, True

    # Split the domain into sub domains.
    split_domain = domain.split('.')
    split_domain.pop(0)

    while split_domain:
        sub_domain = ""

        # Create a sub domain.
        for name in split_domain:
            sub_domain += name
            sub_domain += '.'

        sub_domain = sub_domain[:-1]

        # Check if the sub domain exists in the cache.
        record = cache.check_record(sub_domain, "NS")

        if record is not None:
            return record, False

        split_domain.pop(0)

    return None


def local_search(domain, request_type):
    """
    Performs a local search in the server's storage.
    :param domain: domain
    :param request_type: request type
    :return: response
    """
    response = {}

    # Handle a request of type A
    if request_type == "A":

        # check if the answer exists in the cache.
        record = cache.check_record(domain, "A")

        if record is not None:
            response["A"] = record
            return response

        else:
            # Look for an NS record instead.
            record, is_final = ns_search(domain)

            if record is not None:
                response["NS"] = record
                # TODO check if there might be a case when an NS record exists, but its ip address record doesn't exist
                glued_record = cache.check_record(record.get_domain(), "A")
                response["A"] = glued_record
                return response

    else:  # Handle a request of type NS
        record, is_final = ns_search(domain)

        if record is not None:
            response["NS"] = record
            # If the NS record is not final, add an ip record as well.
            if not is_final:
                glued_record = cache.check_record(record.get_domain(), "A")
                response["A"] = glued_record
            return response

    # Couldn't find any answer in the local storage.
    return None


def resolve(local_response, client_request):

    # Check if I have another server to ask.
    if not local_response:
        pass  # TODO ask the root

    # Get the info needed to ask the next server.
    record = parse_to_record(local_response)
    dest_ip = record.get_ip()
    dest_port = record.get_port()

    # Send request to the next server.
    s.sendto(client_request, (dest_ip, dest_port))
    response, _ = s.recvfrom(2048)
    print "The next server returned:", response



def handle_request(client_request):
    """
    Handles the client's request.
    :param client_request: request in format: [domain] [type]
    :return: record
    """
    domain, request_type = parse_request(client_request)

    # Perform local server search for answer.
    response = local_search(domain, request_type)

    # If an answer was found.
    if response is not None:
        # Check if the answer is final, or this is not a resolver.
        if len(response) == 1 or not is_resolver:
            return response
        else:  # The response is of length 2 and this is a resolver.
            response = resolve(response)
            return response

    else:  # If no answer was found in the local cache.
        if is_resolver:
            response = resolve(None)
            return response

        else:  # No answer was found, and this is not a resolver
            return None


def check_is_root():
    """
    Checks if this server is a root server.
    :return: boolean
    """
    if source_ip == root_ip and source_port == root_port:
        return True
    return False


# Get command line arguments.
# The format: [is_resolver] [ip:port] [root_ip:root_port] [mappings_path]
is_resolver = parse_is_resolver(sys.argv[1])
source_ip, source_port = parse_ip_port(sys.argv[2])
root_ip, root_port = parse_ip_port(sys.argv[3])
file_path = sys.argv[4]

# Check if this server is a root
is_root = check_is_root()

# Create a cache
cache = Cache()
cache.load_file(file_path)

# Create a UDP socket.
s = socket(AF_INET, SOCK_DGRAM)

# Bind socket
s.bind((source_ip, source_port))

while True:
    request, sender_info = s.recvfrom(2048)
    print "Message: ", request, " from: ", sender_info
    answer = handle_request(request)
    str_answer = parse_answer(answer)
    s.sendto(str_answer, sender_info)
