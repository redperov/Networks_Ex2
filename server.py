from cache import Cache


class Server(object):
    def __init__(self, is_resolver, file_path):
        """
        Constructor.
        :param is_resolver: is the server a resolver
        :param file_path: mappings file path
        """
        if is_resolver == "y":
            self._is_resolver = True
        else:
            self._is_resolver = False

        # Load initial data into the cache from the mappings file.
        self._cache = Cache()
        self._cache.load_file(file_path)

    def handle_request(self, request):
        """
        Handles the client's request.
        :param request: request in format: [domain] [type]
        :return: record
        """
        name, request_type = request.split()

        # check if the answer exists in the cache.
        record = self._cache.check_record(name, request_type)

        if record is not None:
            return record
        elif self._is_resolver:
            pass  # TODO implement
        else:
            pass  # TODO implement



