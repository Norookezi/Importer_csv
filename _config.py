from typing import List, Any
from os.path import dirname, join as os_join
from fnmatch import fnmatch

class Field:
    __name__: str = None
    __field__: str = None
    __mandatory__: bool = False
    __unique__: bool = False
    __default__: str = None
    __type__: str = None

    def __init__(self, field):
        self.name(field["csv"])
        self.field(field["name"])
        self.mandatory(field.get("mandatory") or False)
        self.unique(field.get("unique") or False)
        self.default(field.get("default"), '')
        self.type(field.get("type"), '')

    def __get_name__(self) -> str:return self.__name__
    def __get_field__(self) -> str:return self.__field__
    def __get_mandatory__(self) -> bool:return self.__mandatory__
    def __get_unique__(self) -> bool:return self.__unique__
    def __get_default__(self) -> bool:return self.__default__
    def __get_type__(self) -> bool:return self.__type__

    def __set_name__(self, name: str) -> None: self.__name__ = name
    def __set_field__(self, field: str) -> None: self.__field__ = field
    def __set_mandatory__(self, mandatory: bool = False) -> None: self.__mandatory__ = mandatory
    def __set_unique__(self, unique: bool = False) -> None: self.__unique__ = unique
    def __set_default__(self, default: bool = False) -> None: self.__default__ = default
    def __set_type__(self, type: bool = False) -> None: self.__type__ = type

    name = property(__get_name__, __set_name__)
    field = property(__get_field__, __set_field__)
    mandatory = property(__get_mandatory__, __set_mandatory__)
    unique = property(__get_unique__, __set_unique__)
    default = property(__get_default__, __set_default__)
    type = property(__get_type__, __set_type__)


class Config:
    __name__: str = None
    __file__: str = None
    __pattern__: str = None
    __method__: str = None
    __fields__: List[Field] = []
    __database__: str = None
    __table__: str = None
    __separator__: str = None

    def __get_name__(self) -> str: return self.__name__
    def __get_file__(self) -> str: return self.__file__
    def __get_pattern__(self) -> str: return self.__pattern__
    def __get_method__(self) -> str: return self.__method__
    def __get_fields__(self) -> List[Field]: return self.__fields__
    def __get_database__(self) -> str: return self.__database__
    def __get_table__(self) -> str: return self.__table__
    def __get_separator__(self) -> str: return self.__separator__

    def __set_name__(self, name: str) -> None: self.__name__ = name
    def __set_file__(self, file: str) -> None: self.__file__ = file
    def __set_pattern__(self, pattern: str) -> None: self.__pattern__ = pattern
    def __set_method__(self, method: str) -> None: self.check_method(method)
    def __set_fields__(self, fields: Any) -> None: self.__fields__ = fields
    def __set_database__(self, database: str) -> None: self.__database__ = database
    def __set_table__(self, table: str) -> None: self.__table__ = table
    def __set_separator__(self, separator: str) -> None: self.__separator__ = separator

    def check_method(self, method) -> bool:
        accepted_methods = ["add_or_cancel","add_or_pass","add_or_duplicate","add_or_replace","update_or_pass","update_or_cancel","update_or_add"]

        if not method in accepted_methods:
            raise ValueError("Invalid method '{method}'".format(method=str(method)))

        self.__method__ = method

    def add_fields(self, fields):
        self.fields.append(Field(fields))

    def path_match(self, path: str) -> bool:
        pattern = os_join(dirname(self.file), self.pattern)

        return fnmatch(path, pattern)

    name = property(__get_name__, __set_name__)
    file = property(__get_file__, __set_file__)
    pattern = property(__get_pattern__, __set_pattern__)
    method = property(__get_method__, __set_method__)
    fields = property(__get_fields__, __set_fields__)
    database = property(__get_database__, __set_database__)
    table = property(__get_table__, __set_table__)
    separator = property(__get_separator__, __set_separator__)