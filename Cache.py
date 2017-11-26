class Cache:

    def __init__(self):
        self._dictionary = {}

    def load_file(self):
        """
        Loads all the data from the mappings file into the cache.
        :return: None
        """
        with open("mappings.txt", "r") as mappings_file:
            for line in mappings_file:
                new_record = line.split()
                # store the domain as the key, and the rest as value.
                self._dictionary[new_record[0]] = new_record[1:]
