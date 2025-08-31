import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue

class AutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path, event_queue):
        self.repo_path = Path(repo_path)
        self.event_queue = event_queue

    def on_modified(self, event):
        if not event.is_directory:
            self.event_queue.put(('modified', str(event.src_path)))

    def on_created(self, event):
        if not event.is_directory:
            self.event_queue.put(('created', str(event.src_path)))

    def on_deleted(self, event):
        if not event.is_directory:
            self.event_queue.put(('deleted', str(event.src_path)))

class FileWatcher:
    def __init__(self, repo_path, event_queue):
        self.repo_path = repo_path
        self.event_queue = event_queue
        self.observer = Observer()
        self.handler = AutoCommitHandler(repo_path, event_queue)
        self.observer.schedule(self.handler, path=repo_path, recursive=True)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
