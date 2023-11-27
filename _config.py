from typing import *

class Field:
    __name__: str = None
    __field__: str = None
    __mandatory__: bool = False
    __unique__: bool = False
    
    def __get_name__(self) -> str:return self.name
    def __get_field__(self) -> str:return self.field
    def __get_mandatory__(self) -> bool:return self.mandatory
    def __get_unique__(self) -> bool:return self.unique
    
    def __set_name__(self, name: str) -> None: self.__name__ = name
    def __set_field__(self, field: str) -> None: self.__field__ = field
    def __set_mandatory__(self, mandatory: bool = False) -> None: self.__mandatory__ = mandatory
    def __set_unique__(self, unique: bool = False) -> None: self.__unique__ = unique
    
    name = property(__get_name__, __set_name__)
    field = property(__get_field__, __set_field__)
    mandatory = property(__get_mandatory__, __set_mandatory__)
    unique = property(__get_unique__, __set_unique__)
    
    
class Config:
    __name__: str = None
    __file__: str = None
    __pattern__: str = None
    __method__: str = None
    __fields__: List[Field] = None
    
    def __get_name__(self) -> str: return self.__name__
    def __get_file__(self) -> str: return self.__file__
    def __get_pattern__(self) -> str: return self.__pattern__
    def __get_method__(self) -> str: return self.__method__
    def __get_fields__(self) -> List[Field]: return self.__fields__
    
    def __set_name__(self, name: str) -> None: self.__name__ = name
    def __set_file__(self, file: str) -> None: self.__file__ = file
    def __set_pattern__(self, pattern: str) -> None: self.__pattern__ = pattern
    def __set_method__(self, method: str) -> None: self.check_method(method)
    def __set_fields__(self, fields: Any) -> None: self.__fields__ = fields
    
    def check_method(self, method) -> bool:
        accepted_methods = ["add_or_cancel","add_or_pass","add_or_duplicate","add_or_replace","update_or_pass","update_or_cancel","update_or_add"]
        
        if not method in accepted_methods:
            raise ValueError("Invalid method {method}".format(method=str(method)))
        
        self.__method__ = method
       
     
    name = property(__get_name__, __set_name__)
    file = property(__get_file__, __set_file__)
    pattern = property(__get_pattern__, __set_pattern__)
    method = property(__get_method__, __set_method__)
    fields = property(__get_fields__, __set_fields__)