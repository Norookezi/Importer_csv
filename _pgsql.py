import psycopg2
from typing import Any
from _config import Config

class PG_session:
    __database__: str = None
    __host__: str = None
    __user__: str = None
    __password__: str = None
    __port__: int = None

    __connection__ = None
    __cursor__ = None

    error: Any = None

    def __get_database__(self) -> str: return self.__database__
    def __get_host__(self) -> str: return self.__host__
    def __get_user__(self) -> str: return self.__user__
    def __get_password__(self) -> None: return
    def __get_port__(self) -> int: return self.__port__

    def __get_connection__(self): return self.__connection__
    def __get_cursor__(self):
        if self.__cursor__ == None:
            self.cursor = self.connection.cursor()

        return self.__cursor__

    def __set_database__(self, database: str = None): self.__database__ = database
    def __set_host__(self, host: str = None): self.__host__ = host
    def __set_user__(self, user: str = None): self.__user__ = user
    def __set_password__(self, password: str = None): self.__password__ = password
    def __set_port__(self, port: str = None): self.__port__ = int(port)
    def __set_cursor__(self, cursor): self.__cursor__ = cursor
    def __set_connection__(self, connection): self.__connection__ = connection

    database = property(__get_database__, __set_database__)
    host = property(__get_host__, __set_host__)
    user = property(__get_user__, __set_user__)
    password = property(__get_password__, __set_password__)
    port = property(__get_port__, __set_port__)
    connection = property(__get_connection__, __set_connection__)
    cursor = property(__get_cursor__, __set_cursor__)

    def __init__(self, database: str = None, host: str = None, user: str = None, password: str = None, port: str = None) -> None:
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        
        try:
            self.set_connection()
        except Exception as e:
            raise ConnectionError("Connection error: %s" % e)

    def __del__(self) -> None:
        if self.error is None:
            self.commit()
            
        else:
            self.rollback()
            self.connection.rollback()

        self.cursor.close()

    def set_connection(self):
        self.connection = psycopg2.connect(
            database=self.__database__,
            host=self.__host__,
            user=self.__user__,
            password=self.__password__,
            port=self.__port__
        )

    def commit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()

    def exec(self, request):
        self.cursor.execute(request)
        
    def get(self): return self.cursor.fetchall()
    def get_one(self): return self.cursor.fetchone()[0]
    
    def count(self): return self.cursor.rowcount
