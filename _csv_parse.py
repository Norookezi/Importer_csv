from typing import List
from _config import Config

class Line:
    def __init__(self, headers, values):
        for index, value in enumerate(values):
            setattr(self, headers[index], value)

class Csv_parse:
    __separator__ = None
    __file__ = None
    __rule__: Config = None
    header = []
    lines: List[Line] = []
    
    def __init__(self, path: str = None, separator: str = ";"):
        self.__separator__ = separator
        self.__file__ = path
        
        self.get_content()
        
    def get_content(self):
        file = open(self.__file__, 'r', encoding='utf-8')
        content = file.read().split('\n')
        self.header = content[0].split(self.__separator__)
        self.set_lines(content[1:])
        
        print(self.lines)
        
    def set_lines(self, lines):
        for line in lines:
            self.lines.append(Line(self.header, line.split(self.__separator__)))
            
if __name__ == '__main__':
    Csv_parse('./test.csv')