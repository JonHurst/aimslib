#!/usr/bin/python3

import unittest
import datetime
import aimslib.detailed_roster.process as p
import aimslib.common.types as T

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
        expected_result = (
            T.Duty(
                T.TripID('13800', '6275'),
                datetime.datetime(2017, 10, 13, 5, 0),
                datetime.datetime(2017, 10, 13, 15, 13),
                (
                    T.Sector('6275', 'BRS', 'KRK',
                           datetime.datetime(2017, 10, 13, 6, 10),
                           datetime.datetime(2017, 10, 13, 8, 30),
                           datetime.datetime(2017, 10, 13, 6, 10),
                           datetime.datetime(2017, 10, 13, 8, 30),
                           None, None, T.SectorFlags.NONE,
                           '201710136275~'),
                    T.Sector('6276', 'KRK', 'BRS',
                           datetime.datetime(2017, 10, 13, 9, 7),
                           datetime.datetime(2017, 10, 13, 11, 38),
                           datetime.datetime(2017, 10, 13, 9, 7),
                           datetime.datetime(2017, 10, 13, 11, 38),
                           None, None, T.SectorFlags.NONE,
                           '201710136276~'),
                    T.Sector('566', 'BRS', 'NCL',
                           datetime.datetime(2017, 10, 13, 12, 10),
                           datetime.datetime(2017, 10, 13, 13, 3),
                           datetime.datetime(2017, 10, 13, 12, 10),
                           datetime.datetime(2017, 10, 13, 13, 3),
                           None, None, T.SectorFlags.NONE,
                           '20171013566~'),
                    T.Sector('565', 'NCL', 'BRS',
                           datetime.datetime(2017, 10, 13, 13, 40),
                           datetime.datetime(2017, 10, 13, 14, 43),
                           datetime.datetime(2017, 10, 13, 13, 40),
                           datetime.datetime(2017, 10, 13, 14, 43),
                           None, None,
                           T.SectorFlags.NONE,
                           '20171013565~')
                )),
            T.Duty(
                T.TripID('13804', '6195'),
                datetime.datetime(2017, 10, 17, 4, 30),
                datetime.datetime(2017, 10, 17, 15, 18),
                (
                    T.Sector('6195', 'BRS', 'LPA',
                           datetime.datetime(2017, 10, 17, 5, 40),
                           datetime.datetime(2017, 10, 17, 10, 7),
                           datetime.datetime(2017, 10, 17, 5, 40),
                           datetime.datetime(2017, 10, 17, 10, 7),
                           None, None, T.SectorFlags.NONE,
                           '201710176195~'),
                    T.Sector('6196', 'LPA', 'BRS',
                           datetime.datetime(2017, 10, 17, 11, 7),
                           datetime.datetime(2017, 10, 17, 14, 48),
                           datetime.datetime(2017, 10, 17, 11, 7),
                           datetime.datetime(2017, 10, 17, 14, 48),
                           None, None, T.SectorFlags.NONE,
                           '201710176196~')
                )))
        self.assertEqual(p.duty_list(data), expected_result)


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
        expected_result = (
            T.Duty(
                T.TripID('13809', 'LSBY'),
                datetime.datetime(2017, 10, 22, 10, 0),
                datetime.datetime(2017, 10, 22, 21, 40),
                (
                    T.Sector('LSBY', None, None,
                             datetime.datetime(2017, 10, 22, 10, 0),
                             datetime.datetime(2017, 10, 22, 18, 0),
                             datetime.datetime(2017, 10, 22, 10, 0),
                             datetime.datetime(2017, 10, 22, 18, 0),
                             None, None,
                             T.SectorFlags.QUASI| T.SectorFlags.GROUND_DUTY,
                             None),
                    T.Sector('6140', 'TLS', 'BRS',
                             datetime.datetime(2017, 10, 22, 19, 28),
                             datetime.datetime(2017, 10, 22, 21, 25),
                             datetime.datetime(2017, 10, 22, 19, 28),
                             datetime.datetime(2017, 10, 22, 21, 25),
                             None, None,
                             T.SectorFlags.POSITIONING,
                             '201710226140~'))),)
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
        expected_result = (
            T.Duty(
                T.TripID('13453', '6073R'),
                datetime.datetime(2016, 10, 31, 15, 30),
                datetime.datetime(2016, 11, 1, 0, 0),
                (
                    T.Sector('6073R', 'BRS', 'BRS',
                             datetime.datetime(2016, 10, 31, 16, 30),
                             datetime.datetime(2016, 10, 31, 16, 45),
                             datetime.datetime(2016, 10, 31, 16, 30),
                             datetime.datetime(2016, 10, 31, 16, 45),
                             None, None, T.SectorFlags.NONE,
                             '201610316073R~'),
                    T.Sector('6073', 'BRS', 'ALC',
                             datetime.datetime(2016, 10, 31, 18, 43),
                             datetime.datetime(2016, 10, 31, 21, 4),
                             datetime.datetime(2016, 10, 31, 18, 43),
                             datetime.datetime(2016, 10, 31, 21, 4),
                             None, None, T.SectorFlags.NONE,
                             '201610316073~'),
                    T.Sector('6074', 'ALC', '???',
                             datetime.datetime(2016, 10, 31, 21, 39),
                             datetime.datetime(2016, 11, 1, 0, 0),
                             datetime.datetime(2016, 10, 31, 21, 39),
                             datetime.datetime(2016, 11, 1, 0, 0),
                             None, None,
                             T.SectorFlags.NONE,
                             '201610316074~'))),)
        self.assertEqual(p.duty_list(data), expected_result)
