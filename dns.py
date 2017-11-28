class DnsRequest(object):

    def __init__(self, request):
        """
        Constructor.
        :param request: string in format [domain] [type]
        """
        self._domain, self._type = request.split()

    def get_domain(self):
        """
        Domain getter
        :return: domain name
        """
        return self._domain

    def get_type(self):
        """
        Type getter
        :return: request type
        """
        return self._type


class DnsResponse(object):

    def __init__(self, answer_type):
        self._answer_type = answer_type
        self._a_record = None
        self._ns_record = None
        self._is_final_answer = None

    def add_a_record(self, record):
        self._a_record = record

    def add_ns_record(self, record):
        self._ns_record = record

    def get_answer_type(self):
        return self._answer_type

    def get_a_record(self):
        return self._a_record

    def get_ns_record(self):
        return self._ns_record

    def set_is_final_answer(self, boolean):
        self._is_final_answer = boolean

    def get_is_final_answer(self):
        return self._is_final_answer

    def __str__(self):
        if self._answer_type == "A":
            return self.get_a_record()
        else:
            return self.get_ns_record()
