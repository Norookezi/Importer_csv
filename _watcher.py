from os.path import basename
from watchdog.events import FileSystemEventHandler as Event
from threading import Thread
from datetime import datetime

class Watcher(Event):
    __main__ = None

    def __init__(self, main = None): self.__main__ = main

    def handle_event(self, event: Event) -> None:
        if event.is_directory:
            return

        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Proc: ", basename(event.src_path))
        Thread(target=self.__main__.handle_event, args=(event,)).start()

    on_modified = on_created = on_deleted = handle_event