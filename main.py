import sys, os, re
from multiprocessing.dummy import Pool, cpu_count
from counter import Counter

EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']
WORKER_COUNT = max(cpu_count() - 1, 1)

'''
Augmented files will have names matching the regex below, eg

    original__rot90__crop1__flipv.jpg

'''
AUGMENTED_FILE_REGEX = re.compile('^.*(__[^_]+)+\\.[^\\.]+$')
EXTENSION_REGEX = re.compile('|'.join(map(lambda n : '.*\\.' + n + '$', EXTENSIONS)))

thread_pool = None
counter = None

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

    counter = Counter()
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
