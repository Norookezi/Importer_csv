from time import time
from yaml import safe_load as read_yaml
from os import rename as os_rename, mkdir
from os.path import dirname, basename, join as os_join, exists as path_exist
from _config import Config
from _csv_parse import Csv_parse
from _pgsql import PG_session

class Request:
    request_poll = []
    def insert(self, rule: Config = None, file: Csv_parse = None):

        method = getattr(self, rule.method)

        method(rule, file)

    def add_or_cancel(self, rule: Config, file: Csv_parse)-> None:
        broker_conf = read_yaml(open("./.env.yaml", "r", encoding="utf-8"))
        database = broker_conf['DATABASES'][rule.database]
        session = PG_session(rule.database, database["host"], database["user"], database["pass"], database["port"])

        for index, line in enumerate(file.__lines__):
            request = self.generate_insert(rule, line)

            session.exec(request)

            if session.count() == 0:
                session.error = "Line {} in {} is duplicated and process method is add_or_cancel, rolling back".format(index+2, file.__file__)
            
            self.check_error(session, file)

            self.request_poll.append(request)

        self.done(file)

    def add_or_pass(self, rule: Config, file: Csv_parse)-> None:
        broker_conf = read_yaml(open("./.env.yaml", "r", encoding="utf-8"))
        database = broker_conf['DATABASES'][rule.database]
        session = PG_session(rule.database, database["host"], database["user"], database["pass"], database["port"])

        try:
            for line in file.__lines__:
                request = self.generate_insert(rule, line)

                session.exec(request)

                self.check_error(session, file)

                self.request_poll.append(request)

            self.done(file)
        except Exception as e:
            session.error(str(e))
            self.check_error(session, file)

    def generate_insert(self, rule, line):
        request = """
            INSERT INTO {table} ({fields})
            SELECT {couple_field_value}
            WHERE NOT EXISTS (
                SELECT 1
                FROM {table}
                WHERE {condition}
            );
            """.format(
                    table=rule.table,
                    fields=", ".join([field.field for field in rule.fields]),
                    couple_field_value = ", ".join([
                        "\'{value}\'{type} as {field}".format(
                            value=getattr(line, fields.name, getattr(fields, 'default', '')),
                            field=fields.field,
                            type="::{}".format(fields.type) if fields.type else ""
                        ) for fields in rule.fields
                    ]),
                    condition = " or ".join(["{field} = \'{value}\'".format(value=getattr(line, fields.name), field=fields.field) for fields in rule.fields if fields.unique])
                    )
            
        return request
    
    def check_error(self, session, file):
        if session.error is not None:
            session.rollback()
            if not path_exist(os_join(dirname(file.__file__), "_error")):
                mkdir(os_join(dirname(file.__file__), "_error"))

            if not path_exist(os_join(dirname(file.__file__), "_error", basename(file.__file__))):
                os_rename(file.__file__, os_join(dirname(file.__file__), "_error", basename(file.__file__)))
            else:
                os_rename(file.__file__, os_join(dirname(file.__file__), "_error", basename(file.__file__) + str(time())))
            with open(os_join(dirname(file.__file__), "_error", ".".join(basename(file.__file__).split(".")[:-1]) + ".log"), "w") as log:
                log.write(session.error)
                log.close()
                
            raise ValueError(session.error)
        
    def done(self, file):
        if not path_exist(os_join(dirname(file.__file__), "_done")):
            mkdir(os_join(dirname(file.__file__), "_done"))
                
        if not path_exist(os_join(dirname(file.__file__), "_done", basename(file.__file__))):
            os_rename(file.__file__, os_join(dirname(file.__file__), "_done", basename(file.__file__)))
        else:
            os_rename(file.__file__, os_join(dirname(file.__file__), "_done", basename(file.__file__) + str(time())))
    
    def add_or_duplicate(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")

    def add_or_replace(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")

    def update_or_pass(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")

    def update_or_cancel(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")

    def update_or_add(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")
