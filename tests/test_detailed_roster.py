#!/usr/bin/python3

import unittest
import datetime
import aimslib.detailed_roster.process as p

from aimslib.common.types import TripID

class Test_duty_list(unittest.TestCase):

    def test_standard_trips(self):
        data = [
            [
                p.Event(datetime.date(2017, 10, 13), '6275'),
                datetime.datetime(2017, 10, 13, 5, 0),
                datetime.datetime(2017, 10, 13, 6, 10),
                p.Event(datetime.date(2017, 10, 13), 'BRS'),
                p.Event(datetime.date(2017, 10, 13), 'KRK'),
                datetime.datetime(2017, 10, 13, 8, 30),
                p.Break(0),
                p.Event(datetime.date(2017, 10, 13), '6276'),
                datetime.datetime(2017, 10, 13, 9, 7),
                p.Event(datetime.date(2017, 10, 13), 'KRK'),
                p.Event(datetime.date(2017, 10, 13), 'BRS'),
                datetime.datetime(2017, 10, 13, 11, 38),
                p.Break(0),
                p.Event(datetime.date(2017, 10, 13), '566'),
                datetime.datetime(2017, 10, 13, 12, 10),
                p.Event(datetime.date(2017, 10, 13), 'BRS'),
                p.Event(datetime.date(2017, 10, 13), 'NCL'),
                datetime.datetime(2017, 10, 13, 13, 3),
                p.Break(0),
                p.Event(datetime.date(2017, 10, 13), '565'),
                datetime.datetime(2017, 10, 13, 13, 40),
                p.Event(datetime.date(2017, 10, 13), 'NCL'),
                p.Event(datetime.date(2017, 10, 13), 'BRS'),
                datetime.datetime(2017, 10, 13, 14, 43),
                datetime.datetime(2017, 10, 13, 15, 13)
            ],
            [
                p.Event(datetime.date(2017, 10, 17), '6195'),
                datetime.datetime(2017, 10, 17, 4, 30),
                datetime.datetime(2017, 10, 17, 5, 40),
                p.Event(datetime.date(2017, 10, 17), 'BRS'),
                p.Event(datetime.date(2017, 10, 17), 'LPA'),
                datetime.datetime(2017, 10, 17, 10, 7),
                p.Break(0),
                p.Event(datetime.date(2017, 10, 17), '6196'),
                datetime.datetime(2017, 10, 17, 11, 7),
                p.Event(datetime.date(2017, 10, 17), 'LPA'),
                p.Event(datetime.date(2017, 10, 17), 'BRS'),
                datetime.datetime(2017, 10, 17, 14, 48),
                datetime.datetime(2017, 10, 17, 15, 18)
            ]
        ]
        self.assertEqual(
            p.duty_list(data), [
                [
                    TripID(aims_day='13800', trip='6275'),
                    [
                        datetime.datetime(2017, 10, 13, 5, 0),
                        datetime.datetime(2017, 10, 13, 15, 13)
                    ],
                    [
                        '6275',
                        datetime.datetime(2017, 10, 13, 6, 10),
                        'BRS', 'KRK',
                        datetime.datetime(2017, 10, 13, 8, 30)
                    ],
                    [
                        '6276',
                        datetime.datetime(2017, 10, 13, 9, 7),
                        'KRK', 'BRS',
                        datetime.datetime(2017, 10, 13, 11, 38)
                    ],
                    [
                        '566',
                        datetime.datetime(2017, 10, 13, 12, 10),
                        'BRS', 'NCL',
                        datetime.datetime(2017, 10, 13, 13, 3)
                    ],
                    [
                        '565',
                        datetime.datetime(2017, 10, 13, 13, 40),
                        'NCL', 'BRS',
                        datetime.datetime(2017, 10, 13, 14, 43)
                    ]
                ],
                [
                    TripID(aims_day='13804', trip='6195'),
                    [
                        datetime.datetime(2017, 10, 17, 4, 30),
                        datetime.datetime(2017, 10, 17, 15, 18)],
                    [
                        '6195',
                        datetime.datetime(2017, 10, 17, 5, 40),
                        'BRS', 'LPA',
                        datetime.datetime(2017, 10, 17, 10, 7)
                    ],
                    [
                        '6196',
                        datetime.datetime(2017, 10, 17, 11, 7),
                        'LPA', 'BRS',
                        datetime.datetime(2017, 10, 17, 14, 48)
                    ]
                ]
            ])


    def test_standby_then_postioning(self):
        data = [
            [
                p.Event(datetime.date(2017, 10, 22), 'LSBY'),
                datetime.datetime(2017, 10, 22, 10, 0),
                datetime.datetime(2017, 10, 22, 18, 0),
                p.Break(0),
                p.Event(datetime.date(2017, 10, 22), '6140'),
                datetime.datetime(2017, 10, 22, 18, 10),
                datetime.datetime(2017, 10, 22, 19, 28),
                p.Event(datetime.date(2017, 10, 22), '*TLS'),
                p.Event(datetime.date(2017, 10, 22), 'BRS'),
                datetime.datetime(2017, 10, 22, 21, 25),
                datetime.datetime(2017, 10, 22, 21, 40)
            ]
        ]
        expected_result = [
            [
                TripID(aims_day='13809', trip='LSBY'),
                [
                    datetime.datetime(2017, 10, 22, 10, 0),
                    datetime.datetime(2017, 10, 22, 21, 40)
                ],
                [
                    'LSBY',
                    datetime.datetime(2017, 10, 22, 10, 0),
                    datetime.datetime(2017, 10, 22, 18, 0)
                ],
                [
                    '6140',
                    datetime.datetime(2017, 10, 22, 19, 28),
                    '*TLS',
                    'BRS',
                    datetime.datetime(2017, 10, 22, 21, 25)
                ]
            ]
        ]
        self.assertEqual(p.duty_list(data), expected_result)


    def test_returntostand_then_earlyendofroster(self):
        data = [
            [
                p.Event(datetime.date(2016, 10, 31), '6073R'),
                datetime.datetime(2016, 10, 31, 15, 30),
                datetime.datetime(2016, 10, 31, 16, 30),
                p.Event(datetime.date(2016, 10, 31), 'BRS'),
                p.Event(datetime.date(2016, 10, 31), 'BRS'),
                datetime.datetime(2016, 10, 31, 16, 45),
                p.Break(0),
                p.Event(datetime.date(2016, 10, 31), '6073'),
                datetime.datetime(2016, 10, 31, 18, 43),
                p.Event(datetime.date(2016, 10, 31), 'BRS'),
                p.Event(datetime.date(2016, 10, 31), 'ALC'),
                datetime.datetime(2016, 10, 31, 21, 4),
                p.Break(0),
                p.Event(datetime.date(2016, 10, 31), '6074'),
                datetime.datetime(2016, 10, 31, 21, 39),
                p.Event(datetime.date(2016, 10, 31), 'ALC')
            ]
        ]
        expected_result = [
            [
                TripID(aims_day='13453', trip='6073R'),
                [
                    datetime.datetime(2016, 10, 31, 15, 30),
                    datetime.datetime(2016, 11, 1, 0, 0)
                ],
                [
                    '6073R',
                    datetime.datetime(2016, 10, 31, 16, 30),
                    'BRS',
                    'BRS',
                    datetime.datetime(2016, 10, 31, 16, 45)],
                [
                    '6073',
                    datetime.datetime(2016, 10, 31, 18, 43),
                    'BRS',
                    'ALC',
                    datetime.datetime(2016, 10, 31, 21, 4)],
                [
                    '6074',
                    datetime.datetime(2016, 10, 31, 21, 39),
                    'ALC',
                    '???',
                    datetime.datetime(2016, 11, 1, 0, 0)]
            ]
        ]
        self.assertEqual(p.duty_list(data), expected_result)
