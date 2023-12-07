from os.path import basename
from watchdog.events import FileSystemEventHandler as Event
from threading import Thread
from datetime import datetime
threads = []
threads_buffer = []
MAX_THREADS = 2    

class Watcher(Event):
    __main__ = None

    def __init__(self, main = None):
        self.__main__ = main
        Thread(target=self.watch_thread_loop).start()

    def handle_event(self, event: Event) -> None:
        if event.is_directory:
            return
        thread = Thread(target=self.__main__.handle_event, args=(event,), name=basename(getattr(event, "dest_path", event.src_path)))
        threads_buffer.append({'thread': thread, 'status': 'stopped'})

    def start_thread(self, thread):
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Proc: ", basename(thread.name))
        #print("Starting thread ", thread.name, ' ', '0{}'.format(len(threads))[-2:], '/', MAX_THREADS, ' threads alive', sep="")

    def done_thread(self, thread):
        print(datetime.now().strftime("%d/%m %H:%M:%S |"), "Done: ", basename(thread.name))
        #print("Killing thread ", thread.name, ' ', '0{}'.format(len(threads))[-2:], '/', MAX_THREADS, ' threads alive', sep="")
                
    def watch_thread_loop(self):
        while True:
            if len(threads) < MAX_THREADS and len(threads_buffer) != 0:
                threads.append(threads_buffer.pop())

            for index, thread in enumerate(threads):
                if thread["status"] == "stopped":
                    thread["status"] = "started"
                    thread["thread"].start()
                    self.start_thread(thread["thread"])
                elif not thread["thread"].is_alive():
                    self.done_thread(thread["thread"])
                    del threads[index]
                
        
    on_modified = on_created = on_deleted = on_moved = handle_event
