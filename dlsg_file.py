import logging
from copy import deepcopy


class DlsgFile:
    LENGTH_SIZE = 4
    HEADER2021 = "DLSG            Decl20210103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    FOOTER = '\0'
    SECTION_PREFIX = '@'
    merge_list = {
        '@DeclForeign': '@CurrencyIncome'
    }

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

    # Appends data from another DlsgFile object referred by dlsg parameter into current object
    # Only sections from self.merge_list are processed
    def append(self, dlsg):
        for section in self.merge_list:
            dst = self.get_section(section)
            dst_size = dst.get_child_count()
            if dst_size:
                section_to_continue = self.get_section(self.merge_list[section] + f"{(dst_size - 1):04d}")
            else:
                logging.debug("No foreign incomes in source file")
                section_to_continue = self.get_section(section)
            last_idx = self._sections.index(section_to_continue)
            src = dlsg.get_section(section)
            src_size = src.get_child_count()
            for i in range(src_size):
                child = dlsg.get_section(self.merge_list[section] + f"{i:04d}")
                new_child = deepcopy(child)
                new_child.update_tag(self.merge_list[section] + f"{(dst_size + i):04d}")
                self._sections.insert(last_idx + 1, new_child)
                last_idx += 1
            dst.set_child_count(dst_size + src_size)

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

    # Returns section from current data structure
    def get_section(self, section_name):
        section = [section for section in self._sections if section.tag() == section_name]
        if len(section) == 0:
            raise ValueError(f"Section {section_name} was not found")
        if len(section) > 1:
            raise ValueError(f"Multiple match for {section_name} found")
        return section[0]

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

    def update_tag(self, new_tag):
        self._tag = new_tag

    def write(self, records):
        records.append(self._tag)
        records.extend(self._records)

    # Returns a number of next elements that belongs to this section
    def get_child_count(self) -> int:
        try:
            count = int(self._records[0])
        except ValueError:
            raise ValueError("Can't get number of elements")
        return count

    def set_child_count(self, number):
        self._records[0] = str(number)
