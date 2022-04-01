import logging

class DlsgFile:
    HEADER2021 = "DLSG            Decl20210103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"

    # Loads data from given file into internal class structures
    def __init__(self, filename):
        self._filename = filename
        logging.debug(f"Loading file: {filename}")

        with open(self._filename, "r", encoding='cp1251') as taxes:
            raw_data = taxes.read()
        self.header = raw_data[:len(self.HEADER2021)]
        if self.header != self.HEADER2021:
            raise ValueError("Unsupported format of declaration file")

    # Appends data from another DlsgFile object referred by dlsg parameter
    def append(self, dlsg):
        pass

    # Saves current data into initial file
    def save(self):
        pass
