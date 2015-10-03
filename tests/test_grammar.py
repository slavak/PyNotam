import unittest
from notam import grammar
from test_helper import read_test_data


class GrammarParse(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GrammarParse, self).__init__(*args, **kwargs)
        self.test_data = read_test_data()

    def try_parse_all(self, rule, items):
        for i in items:
            try:
                r = grammar[rule].parse(i)
                # print(r)
            except:
                print('Starting at rule "{}", failed to parse:\n{}'.format(rule, i))
                raise

    def test_header(self):
        headers = [d[0] for d in self.test_data]
        headers = [h[1:] for h in headers] # remove opening parenthesis
        self.try_parse_all('header', headers)

    def test_qclause(self):
        qlines = [d[1] for d in self.test_data]
        self.try_parse_all('q_clause', qlines)

    def test_aclause(self):
        alines = [d[2] for d in self.test_data]
        alines = [d[:d.find(' B)')] for d in alines]
        self.try_parse_all('a_clause', alines)

    def test_bclause(self):
        blines = [d[2] for d in self.test_data]
        blines = [d[d.find('B)'):d.find(' C)')] for d in blines]
        self.try_parse_all('b_clause', blines)

    def test_cclause(self):
        clines = [d[2] for d in self.test_data]
        clines = [d[d.find('C)'):] for d in clines]
        self.try_parse_all('c_clause', clines)

    def test_root(self):
        notams = ['\n'.join(d) for d in self.test_data]
        self.try_parse_all('root', notams)


if __name__ == '__main__':
    unittest.main()
