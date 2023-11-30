from _config import Config
from _csv_parse import Csv_parse
from _requests import Request
# Imports
from typing import List, Any
from glob import glob
from os.path import realpath as os_realpath, basename, dirname, join as os_join, exists as file_exist
from watchdog.events import FileSystemEventHandler as Event
from yaml import safe_load as read_yaml
from datetime import datetime

class Process:
    __rules__: {str, List[Config]} = {}
    __rules_path__: str = None
    __conf__: Any = None

    def __init__(self, conf):
        self.__conf__ = conf

        self.__rules_path__ = "{}/*/*.yaml".format(self.__conf__.get('FILES_PATH', None))

        config_files = glob(self.__rules_path__)

        for config_file in config_files: self.get_rules(config_file)      

    def get_rules(self, config_file):
        if basename(config_file).startswith('_'): return

        config = read_yaml(open(config_file, 'r', encoding='utf-8'))
        for conf_name, conf_option in config.items():
            try:
                conf = Config()
                conf.fields = []
                conf.name = conf_name
                conf.file = config_file
                conf.pattern = conf_option["pattern"]
                conf.method = conf_option["method"]

                for name, field in conf_option["fields"].items():
                    conf.add_fields({**field, "csv": name})

                conf.database = conf_option["database"] if "database" in conf_option.keys() else ""
                conf.table = conf_option["table"]

                conf.separator = conf_option["separator"] if "separator" in conf_option.keys() else ";"


                replace_allowed = True
                if conf.name in self.__rules__.keys():
                    replace_allowed = self.__conf__.get('REPLACE_DUPLICATES_RULES', False)
                    print('Rules {rule_name} already exists replace: {do_replace}'.format(rule_name=conf.name, do_replace=self.__conf__.get('REPLACE_DUPLICATES_RULES', replace_allowed)))

                if replace_allowed and not basename(config_file).startswith('_'):
                    self.__rules__[conf.name] = conf     
            except (KeyError, ValueError) as e:
                print("⚠️ - ERROR OCCURRED ({error}) | Can't process {file}".format(error=e, file=os_realpath(config_file)))

    def file_modified(self, path: str):

        #Ignored file
        if basename(path).startswith('_'):
            self.remove_ignored_rules(os_join(dirname(path), basename(path)[1:]))
            print(self.__rules__)
        else: 
            self.get_rules(path)
            self.remove_deleted_key(path)


    def remove_deleted_key(self, path: str):
        path_file_content = read_yaml(open(os_realpath(path), "r", encoding="utf-8")).keys() if path else []
        self.delete_rule(lambda name, conf: (os_realpath(conf.file) == os_realpath(path) and name not in path_file_content))        
    def remove_ignored_rules(self, ignore_file_path):
        self.delete_rule(lambda name, conf: os_realpath(conf.file) == os_realpath(ignore_file_path))
    def delete_orphan_rules(self, path: str = None, config: List[str] = None):
        self.delete_rule(lambda name, conf: not file_exist(os_realpath(conf.file)))

    def delete_rule(self, condition) -> List[str]:
        to_delete: List[str] = [conf_name for conf_name, conf in self.__rules__.items() if condition(conf_name, conf)]
        self._to_delete(to_delete)
    def _to_delete(self, delete_keys: List[str] = None):
        for name in delete_keys:
            del self.__rules__[name]

    def handle_event(self, event: Event):
        event_path = getattr(event, "dest_path", event.src_path)
        if basename(event_path).endswith('.yaml'):
            if event.event_type == "deleted":
                self.delete_orphan_rules(event.src_path)

            elif event.event_type == "modified":
                self.file_modified(event.src_path)

        elif basename(event_path).endswith('.csv'):
            if "_error" in dirname(event_path) or\
                "_done" in dirname(event_path) or\
                event.event_type == "deleted":
                return self.done(event)

            rule = [rule for rule in self.__rules__.values() if rule.path_match(event_path)]

            if len(rule) == 0:
                print("File not processed, no rule for this name")
                self.done(event)
                return

            file: Csv_parse = Csv_parse(event_path, rule[0].__separator__, rule[0].fields)

            request = Request()
            request.insert(rule = rule[0], file = file)

        else:
            print("File not processed, {} isn't a valid format".format(basename(event_path).split('.')[-1]))
        self.done(event)


    def done(self, event) -> None:
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Done: ", basename(event.src_path))