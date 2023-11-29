from typing import List
from _config import Config

class Line:
    __values__ = {}
    
    def parse(self, headers, values):
        for index, value in enumerate(values):
            setattr(self, headers[index], value)
        return (self)

class Csv_parse:
    __separator__ = None
    __file__ = None
    __rule__: Config = None
    __header__: List[str] = []
    __lines__: List[Line] = []
    
    def __init__(self, path: str = None, separator: str = ";"):
        self.__separator__ = separator
        self.__file__ = path
        
        self.get_content()
        
    def get_content(self):
        file = open(self.__file__, 'r', encoding='utf-8')
        content = file.read().split('\n')
        self.__header__ = content[0].split(self.__separator__)
        
        self.set_lines(content[1:])
        
    def set_lines(self, lines):
        self.__lines__ = []
        for line in lines:
            lineInstance = Line()
            test = lineInstance.parse(self.__header__, line.split(self.__separator__))
            self.__lines__.append(test)
            
if __name__ == '__main__':
    print(Csv_parse('./test.csv').__dict__)