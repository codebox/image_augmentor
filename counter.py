from multiprocessing.dummy import Lock

class Counter:
    def __init__(self):
        self.lock = Lock()
        self._processed = 0
        self._error = 0
        self._skipped_no_match = 0
        self._skipped_augmented = 0

    def processed(self):
        with self.lock:
            self._processed += 1

    def error(self):
        with self.lock:
            self._error += 1

    def skipped_no_match(self):
        with self.lock:
            self._skipped_no_match += 1

    def skipped_augmented(self):
        with self.lock:
            self._skipped_augmented += 1

    def get(self):
        with self.lock:
            return {'processed' : self._processed, 'error' : self._error, 'skipped_no_match' : self._skipped_no_match, 'skipped_augmented' : self._skipped_augmented}
