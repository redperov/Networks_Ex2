class Cache(object):
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
                # Add new record to the records dictionary.
                new_record = Record(line[0], line[1], line[2], line[3])
                self.add_record(new_record)

    def add_record(self, record):
        """
        Adds a new record to the cache
        :param record: a new record
        :return: None
        """
        # Store the domain as the key, and the rest as value.
        new_key = "{0},{1}".format(record.get_domain(), record.get_record_type())
        self._records[new_key] = record
        print new_key

    def check_record(self, domain, request_type):
        """
        Looks for the record in the cache.
        :param domain: domain name
        :param request_type: request type
        :return: record
        """
        key = "{0},{1}".format(domain, request_type)
        if key in self._records:
            return self._records[key]
        return None


class Record(object):
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
        self._ttl = int(ttl)

        self._check_ip_port_split()

    def _check_ip_port_split(self):
        """
        Checks if the record is of type A, then splits to ip and port.
        :return: None
        """
        if self._type == "A":
            formatted_value = self._value.split(':')
            self._ip = formatted_value[0]
            self._port = int(formatted_value[1])

    def get_domain(self):
        """
        Domain name getter
        :return: domain
        """
        return self._domain

    def get_record_type(self):
        """
        record type getter
        :return: record type
        """
        return self._type

    def get_value(self):
        """
        value getter
        :return: value
        """
        return self._value

    def get_ip(self):
        """
        Ip getter.
        :return: ip address
        """
        return self._ip

    def get_port(self):
        """
        Port number getter
        :return: port number
        """
        return self._port

    def get_ttl(self):
        """
        TTL getter
        :return: ttl
        """
        return self._ttl

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.get_domain(), self.get_record_type(), self.get_value(), self.get_ttl())
