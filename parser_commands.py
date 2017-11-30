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


def parse_answer(dictionary_answer):
    """
    Parses a dictionary into a string format.
    :param dictionary_answer: dictionary
    :return: string format of a dictionary
    """
    if dictionary_answer:
        str_answer = ""
        for item in dictionary_answer:
            str_answer += str(dictionary_answer[item])
            str_answer += '\n'
        str_answer = str_answer[: -1]
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


def parse_to_dictionary(str_input):

    records = {}
    split_input = str_input.split('\n')

    for item in split_input:

        # Check if item is a valid field.
        if item != "":
            # Split to record fields.
            split_item = item.split()

            if split_item[1] == "A":
                records["A"] = item
            else:
                records["NS"] = item

    return records
