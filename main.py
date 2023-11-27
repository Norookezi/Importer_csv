# Imports
from typing import List
from fnmatch import fnmatch as wildcard
from glob import glob
from os.path import realpath as os_realpath, basename, dirname, join as os_join, exists as file_exist
from watchdog.events import FileSystemEventHandler as Event
from watchdog.observers import Observer
from yaml import safe_load as read_yaml
from threading import Thread
from datetime import datetime

# Local import
from _config import Config

config_file = open("./.env.yaml", "r", encoding="utf-8")
broker_conf = read_yaml(config_file)
        
class Main:
    __rules__: {str, List[Config]} = {}
    __rules_path__: str = None
    
    def __init__(self, conf):
        self.__rules_path__ = conf.get('RULES_PATH', None)
        
        config_files = glob(self.__rules_path__)
        
        for config_file in config_files: self.get_rules(config_file)
        
        for name, rule in self.__rules__.items():
            print("{}\n   {}".format(name, rule.__dict__))          
    def get_rules(self, config_file):
        config = read_yaml(open(config_file, 'r', encoding='utf-8'))
        for conf_name, conf_option in config.items():
            conf = Config()
            conf.name = conf_name
            conf.file = config_file
            conf.pattern = conf_option["pattern"]
            conf.method = conf_option["method"]
            
            replace_allowed = True
            if conf.name in self.__rules__.keys():
                replace_allowed = broker_conf.get('REPLACE_DUPLICATES_RULES', False)
                print('Rules {rule_name} already exists replace: {do_replace}'.format(rule_name=conf.name, do_replace=broker_conf.get('REPLACE_DUPLICATES_RULES', replace_allowed)))

            if replace_allowed and not basename(config_file).startswith('_'):
                self.__rules__[conf.name] = conf        
        print(self.__rules__)
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
            
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Done: ", basename(event.src_path))
        
main = Main(broker_conf)

class Watcher(Event):
    def handle_event(self, event: Event) -> None:
        if event.is_directory:
            return
        
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Proc: ", basename(event.src_path))
        Thread(target=main.handle_event, args=(event,)).start()

    on_modified = on_created = on_deleted = handle_event

observer = Observer()
observer.schedule(Watcher(), broker_conf["FILES_PATH"], recursive=True)
observer.start()

try:
    while True:pass
except KeyboardInterrupt:
    observer.stop()

observer.join()