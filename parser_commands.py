def parse_is_resolver(str_input):
    """
    Parses the is resolver answer from string to boolean.
    :param str_input: is resolver string
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


def parse_request(str_input):
    """
    Parses the request into domain and request type
    :param str_input: string input
    :return: domain, request type
    """
    domain, request_type = str_input.split()
    return domain, request_type
