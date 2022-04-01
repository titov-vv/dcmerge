import logging

class DlsgFile:
    LENGTH_SIZE = 4
    HEADER2021 = "DLSG            Decl20210103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    FOOTER = '\0'

    # Loads data from given file into internal class structures
    def __init__(self, filename):
        self._records = []
        self._filename = filename
        logging.debug(f"Loading file: {filename}")

        with open(self._filename, "r", encoding='cp1251') as taxes:
            raw_data = taxes.read()
        self.header = raw_data[:len(self.HEADER2021)]
        if self.header != self.HEADER2021:
            raise ValueError("Unsupported format of declaration file")
        self._split_records(raw_data)

    # Appends data from another DlsgFile object referred by dlsg parameter
    def append(self, dlsg):
        pass

    # Saves current data into initial file
    def save(self):
        pass

    # this method splits declaration data into records stored in self._records
    def _split_records(self, data):
        pos = len(self.HEADER2021)
        while pos < len(data):
            length_field = data[pos: pos + self.LENGTH_SIZE]
            if length_field == (self.FOOTER * len(length_field)):
                self._footer_len = len(length_field)
                break
            try:
                length = int(length_field)
            except Exception as e:
                logging.fatal(f"Invalid record size at position {pos}: '{length_field}'")
                raise e
            pos += self.LENGTH_SIZE
            self._records.append(data[pos: pos + length])
            pos = pos + length
        logging.debug(f"Declaration {self._filename} content: {self._records}")
