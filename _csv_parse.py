from typing import List
from _config import Config, Field

class Line:
    __values__ = {}

    def parse(self, headers, values):
        for index, value in enumerate(values):
            setattr(self, headers[index], value.strip())
        return (self)

class Csv_parse:
    __separator__ = None
    __file__ = None
    __rule__: Config = None
    __header__: List[str] = []
    __lines__: List[Line] = []
    __fields__: List[Field] = []
    __encoding__: str = None

    def __init__(self, path: str = None, separator: str = ";", encoding: str = "utf-8-sig", rule: List[Field] = None):
        self.__separator__ = separator
        self.__file__ = path
        self.__fields__ = rule
        self.__encoding__ = encoding

        self.get_content()

    def get_content(self):
        file = open(self.__file__, 'r', encoding=self.__encoding__)
        content = file.read().split('\n')
        headers = content[0].split(self.__separator__)
        for index, header in enumerate(headers):
            headers[index] = header.strip()
        self.__header__ = headers

        self.set_lines(content[1:])

    def set_lines(self, lines):
        self.__lines__ = []

        for line in lines:
            if len(line) == 0:
                return

            line = line.strip()
            line = line.replace("\"", "")
            line = line.replace("\'", "")

            line_ = Line()

            self.__lines__.append(line_.parse(self.__header__, line.split(self.__separator__)))

        mandatory_fields = [field for field in self.__fields__ if field.__mandatory__ and not field.__name__ in self.__header__]

        if len(mandatory_fields) != 0:
            raise ValueError("Missing fields: %s" % "; ".join([missing_fields.name for missing_fields in mandatory_fields]))
