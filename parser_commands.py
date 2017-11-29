from cache import Record


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


def parse_answer(list_answer):
    """
    Parses the list into a string format.
    :param list_answer: list
    :return: string format of a list
    """
    if list:
        str_answer = '\n'.join(map(str, list_answer))
        return str_answer
    else:
        return "Don't know"


def parse_to_record(str_record):
    """
    Parses a string record into a record object.
    :param str_record: string record
    :return: record
    """
    split_record = str_record.split()
    record = Record(split_record[0], split_record[1], split_record[2], split_record[3])
    return record
