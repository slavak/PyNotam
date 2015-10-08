import os


def read_test_data():
    for (_dirpath, _, _filenames) in os.walk('test_data'):
        filenames = [os.path.join(_dirpath, filename) for filename in _filenames]
        break

    def read_gen(filenames):
        for filename in filenames:
            with open(filename, 'r') as fh:
                yield fh.read().splitlines()

    return list(read_gen(filenames))


def read_single_notam(id):
    """'id' should be either the IAA internal integer identifier, or the NOTAM series and number/year --
    depending on the name of the test_data file containing it."""

    filename = '{}.txt'.format(str(id))
    filename = filename.replace('/', '_')

    with open(os.path.join('test_data', filename), 'r') as fh:
        return fh.read()
