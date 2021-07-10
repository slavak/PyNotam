import datetime
import unittest
import notam
from tests.test_helper import read_single_notam


class TestNotam(unittest.TestCase):
    def test_parsed_fields(self):
        expected_values = {
            'A0623/91' : {
                'notam_id' : 'A0623/91',
                'notam_type' : 'NEW',
                'fir' : 'EGXX',
                'notam_code' : 'QRDCA',
                'traffic_type' : set(['IFR', 'VFR']),
                'purpose' : set(['IMMEDIATE ATTENTION', 'OPERATIONAL SIGNIFICANCE', 'FLIGHT OPERATIONS']),
                'scope' : set(['NAV WARNING']),
                'fl_lower' : 0,
                'fl_upper' : 400,
                'area' : {'lat' : '5510N', 'long' : '00520W', 'radius' : 50},
                'location' : ['EGTT', 'EGPX'],
                'valid_from' : datetime.datetime(1991, 4, 3, 7, 30, tzinfo=datetime.timezone.utc),
                'valid_till' : datetime.datetime(1991, 4, 28, 15, 0, tzinfo=datetime.timezone.utc),
                'schedule' : 'APR 03 07 12 21 24 AND 28 0730 TO 1500',
                'body' : 'DANGER AREA DXX IS ACTIVE',
                'limit_lower' : 'GND',
                'limit_upper' : '12 200 m (40 000 ft) MSL.'
            },
            '476008' : {
                'notam_id' : 'A0126/15',
                'notam_type' : 'REPLACE',
                'ref_notam_id' : 'A0074/14',
                'fir' : 'LLLL',
                'notam_code' : 'QARAU',
                'traffic_type' : set(['IFR', 'VFR']),
                'purpose' : set(['IMMEDIATE ATTENTION', 'OPERATIONAL SIGNIFICANCE', 'FLIGHT OPERATIONS']),
                'scope' : set(['EN-ROUTE']),
                'fl_lower' : 0,
                'fl_upper' : 999,
                'area' : {'lat' : '3250N', 'long' : '03459E', 'radius' : 1},
                'location' : ['LLLL'],
                'valid_from' : datetime.datetime(2015, 1, 13, 9, 1, tzinfo=datetime.timezone.utc),
                'valid_till' : datetime.datetime.max,
                'schedule' : None,
                'body' : 'ATS RTE `H4A` NOT AVBL UFN.',
                'limit_lower' : None,
                'limit_upper' : None
            }
        }

        for (notam_to_test, expected) in expected_values.items():
            notam_text = read_single_notam(notam_to_test)
            n = notam.Notam.from_str(notam_text)
            for (field, value) in expected.items():
                with self.subTest(msg='Field "{}" of NOTAM "{}"'.format(field, notam_to_test)):
                    self.assertEqual(getattr(n, field), value)


if __name__ == '__main__':
    unittest.main()