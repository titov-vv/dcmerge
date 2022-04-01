import logging


class DlsgFile:
    LENGTH_SIZE = 4
    HEADER2021 = "DLSG            Decl20210103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    FOOTER = '\0'
    SECTION_PREFIX = '@'

    # Loads data from given file into internal class structures
    def __init__(self, filename):
        self._records = []
        self._sections = []
        self._footer = ''
        self._filename = filename
        logging.debug(f"Loading file: {filename}")

        with open(self._filename, "r", encoding='cp1251') as taxes:
            raw_data = taxes.read()
        self.header = raw_data[:len(self.HEADER2021)]
        if self.header != self.HEADER2021:
            raise ValueError("Unsupported format of declaration file")
        self._split_records(raw_data)
        self._split_sections()

    # Appends data from another DlsgFile object referred by dlsg parameter
    def append(self, dlsg):
        pass

    # Saves current data into file filename
    def save(self, filename):
        self._records = []
        for section in self._sections:
            section.write(self._records)
        logging.debug(f"Declaration to write: {self._records} +'{self._footer}'")
        raw_data = self.HEADER2021
        for record in self._records:
            raw_data += "{:04d}{}".format(len(record), record)
        raw_data += self._footer
        with open(filename, "w", encoding='cp1251') as taxes:
            taxes.write(raw_data)

    # this method splits declaration data into records stored in self._records
    def _split_records(self, data):
        pos = len(self.HEADER2021)
        while pos < len(data):
            length_field = data[pos: pos + self.LENGTH_SIZE]
            if length_field == (self.FOOTER * len(length_field)):
                self._footer = data[pos:]
                break
            try:
                length = int(length_field)
            except ValueError:
                raise ValueError(f"Invalid record size at position {pos}: '{length_field}'")
            pos += self.LENGTH_SIZE
            self._records.append(data[pos: pos + length])
            pos = pos + length
        logging.debug(f"Declaration {self._filename} content: {self._records} +'{self._footer}'")

    def _split_sections(self):
        while len(self._records) > 0:
            section_name = self._records.pop(0)
            if section_name[0] != self.SECTION_PREFIX:
                raise ValueError(f"Invalid section prefix: {section_name}")
            self._sections.append(DlsgSection(section_name, self._records))
        logging.debug(f"Sections loaded: {[s.tag() for s in self._sections]}")


class DlsgSection:
    SECTION_PREFIX = '@'

    def __init__(self, name, records):
        self._tag = name
        self._records = []
        while (len(records) > 0) and (records[0][:1] != self.SECTION_PREFIX):
            self._records.append(records.pop(0))

    def tag(self) -> str:
        return self._tag

    def write(self, records):
        records.append(self._tag)
        records.extend(self._records)
