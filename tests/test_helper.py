import os


def read_test_data():
    for (_dirpath, _, _filenames) in os.walk("test_data"):
        filenames = [os.path.join(_dirpath, filename) for filename in _filenames]
        break

    def read_gen(filenames):
        for filename in filenames:
            with open(filename, 'r') as fh:
                yield fh.read().splitlines()

    return list(read_gen(filenames))