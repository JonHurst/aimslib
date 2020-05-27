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
