from _config import Config
from _csv_parse import Csv_parse

class Request:
    request_poll = []
    def insert(self, rule: Config = None, file: Csv_parse = None):

        method = getattr(self, rule.method)

        method(self, rule, file)

    def add_or_cancel(self, rule: Config, file: Csv_parse)-> None:
        raise NotImplementedError("Method not implemented yet")

    def add_or_pass(self, rule: Config, file: Csv_parse)-> None:
        unique_fields = [field for field in rule.fields if field.unique]
        print([field for field in rule.fields])
        for line in file.__lines__:
            request = """
            INSERT INTO {database}{table}({fields})
            SELECT {couple_field_value}
            WHERE
            NOT EXISTS (
            	SELECT {fields}
            	FROM {database}{table}
            	WHERE {condition}
            );
            """.format(
                    database=rule.database,
                    table=rule.table,
                    fields=", ".join([field.field for field in rule.fields]),
                    couple_field_value = ", ".join(
                        ["{field} = \"{value}\"".format(value=getattr(line, fields.name), field=fields.field) for fields in rule.fields]),
                    condition = " or ".join(["{field} = \"{value}\"".format(value=getattr(line, fields.name), field=fields.field) for fields in rule.fields if fields.unique])
                    )
            self.request_poll.append(request)
        
        print("\n\n\n\n".join(self.request_poll))

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