import sys, os, re
from multiprocessing.dummy import Pool, cpu_count, Lock

EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']
WORKER_COUNT = max(cpu_count() - 1, 1)

'''
Augmented files will have names matching the regex below, eg

    original__rot90__crop1__flipv.jpg

'''
AUGMENTED_FILE_REGEX = re.compile('^.*(__[^_]+)+\\.[^\\.]+$')
EXTENSION_REGEX = re.compile('|'.join(map(lambda n : '.*\\.' + n + '$', EXTENSIONS)))

thread_pool = None

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

counter = Counter()

def work(d, f):
    counter.processed()
    pass

def process(dir, file):
    thread_pool.apply_async(work, (dir, file))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: {} <image directory>'.format(sys.argv[0])
        sys.exit(1)

    image_dir = sys.argv[1]
    if not os.path.isdir(image_dir):
        print 'Invalid image directory: {}'.format(image_dir)
        sys.exit(2)

    thread_pool = Pool(WORKER_COUNT)
    print 'Thread pool initialised with {} worker{}'.format(WORKER_COUNT, '' if WORKER_COUNT == 1 else 's')

    matches = []
    for dir_info in os.walk(image_dir):
        dir_name, _, file_names = dir_info
        print 'Processing {}...'.format(dir_name)

        for file_name in file_names:
            if EXTENSION_REGEX.match(file_name):
                if AUGMENTED_FILE_REGEX.match(file_name):
                    counter.skipped_augmented()
                else:
                    process(dir_name, file_name)
            else:
                counter.skipped_no_match()

    print "Waiting for workers to complete..."
    thread_pool.close()
    thread_pool.join()

    print counter.get()
