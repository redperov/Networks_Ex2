import sys
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

    return None, False


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
            record, is_final = ns_search(domain)  # TODO remove the boolean if not needed

            if record is not None:
                response["NS"] = record
                # TODO check if there might be a case when an NS record exists, but its ip address record doesn't exist
                glued_record = cache.check_record(record.get_value(), "A")
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


def save_records(records):
    """
    Saves new records in the cache.
    :param records: dictionary of string records.
    :return: None
    """

    for item in records:
        str_record = records[item]
        split_record = str_record.split()
        record = Record(split_record[0], split_record[1], split_record[2], split_record[3])
        cache.add_record(record)


def resolve(local_response, client_request):

    # Check if I can use the local response.
    if local_response:
        # Extract A record from the local response.
        record = local_response["A"]
        # record = parse_to_record(a_record)

        # Get the info needed to ask the next server.
        dest_ip = record.get_ip()
        dest_port = record.get_port()

    elif not is_root:  # No local response, then ask root server.
        dest_ip = root_ip
        dest_port = root_port

    else:  # Root server has not answer
        return None

    # Keep asking other servers until a final answer is received.
    while True:

        # Send request to the next server.
        s.sendto(client_request, (dest_ip, dest_port))
        response, _ = s.recvfrom(2048)
        # TODO delete that
        print "The next server returned:\n", response

        # If the next server didn't have an answer.
        if response == "Don't know":
            return None

        # Parse the answer into a records dictionary.
        response_records = parse_to_dictionary(response)

        # Save received records in the cache. TODO what if received only NS, should I save it?
        save_records(response_records)

        # Check if received the final answer.
        if len(response_records) == 1:
            return response_records  # TODO should I return records instead of strings

        # Extract A record from response records.
        str_record = response_records["A"]

        # Parse string record into record object.
        record = parse_to_record(str_record)

        # Get the info needed to ask the next server.
        dest_ip = record.get_ip()
        dest_port = record.get_port()


def handle_request(client_request):
    """
    Handles the client's request.
    :param client_request: request in format: [domain] [type]
    :return: record
    """
    domain, request_type = parse_request(client_request)

    # Perform a local server search for the closest answer it has.
    response = local_search(domain, request_type)

    # If an answer was found.
    if response is not None:
        # Check if the answer is final, or this is not a resolver.
        if len(response) == 1 or not is_resolver:
            return response
        else:  # The response is of length 2 and this is a resolver.
            response = resolve(response, client_request)
            return response

    else:  # If no answer was found in the local cache.
        if is_resolver:  # If a resolver, ask the root.
            response = resolve(None, client_request)
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
