# Imports
from watchdog.observers.polling import PollingObserver as Observer
from yaml import safe_load as read_yaml

# Local import
from _watcher import Watcher
from _process import Process

broker_conf = read_yaml(open("./.env.yaml", "r", encoding="utf-8"))

main = Process(broker_conf)
watcher = Watcher(main = main)

observer = Observer()
observer.schedule(watcher, broker_conf["FILES_PATH"], recursive=True)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()