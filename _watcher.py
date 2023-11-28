from os.path import basename
from watchdog.events import FileSystemEventHandler as Event
from threading import Thread
from datetime import datetime

class Watcher(Event):
    def handle_event(self, event: Event) -> None:
        if event.is_directory:
            return
        
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Proc: ", basename(event.src_path))
        Thread(target=main.handle_event, args=(event,)).start()

    on_modified = on_created = on_deleted = handle_event