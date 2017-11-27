class Cache:

    def __init__(self):
        """
        Constructor.
        """
        self._records = {}

    def load_file(self, file_path):
        """
        Loads all the data from the mappings file into the cache.
        :return: None
        """
        with open(file_path, "r") as mappings_file:
            for raw_line in mappings_file:
                line = raw_line.split()
                # store the domain as the key, and the rest as value.
                new_record = Record(line[0], line[1], line[2], line[3])
                self._records[new_record.get_domain()] = new_record

    def add_record(self, record):
        """
        Adds a new record to the cache.
        :param record: a new record
        :return: None
        """
        self._records[record.get_domain()] = record


class Record:

    def __init__(self, domain, record_type, value, ttl):
        """
        Constructor.
        :param domain: domain name
        :param record_type: record type
        :param value: record value
        :param ttl: time to live
        """
        self._domain = domain
        self._type = record_type
        self._value = value
        self._ttl = ttl

    def get_domain(self):
        """
        Domain name getter
        :return: domain
        """
        return self._domain

