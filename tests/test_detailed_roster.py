#!/usr/bin/python3

import unittest
import datetime
import aimslib.detailed_roster.process as p
import aimslib.common.types as T

class Test_duty(unittest.TestCase):

    def test_standard_trip(self):
        data = [ p.DStr(datetime.date(2017, 10, 17), '6195'),
                 datetime.datetime(2017, 10, 17, 4, 30),
                 datetime.datetime(2017, 10, 17, 5, 40),
                 p.DStr(datetime.date(2017, 10, 17), 'BRS'),
                 p.DStr(datetime.date(2017, 10, 17), 'LPA'),
                 datetime.datetime(2017, 10, 17, 10, 7),
                 p.Break.LINE,
                 p.DStr(datetime.date(2017, 10, 17), '6196'),
                 datetime.datetime(2017, 10, 17, 11, 7),
                 p.DStr(datetime.date(2017, 10, 17), 'LPA'),
                 p.DStr(datetime.date(2017, 10, 17), 'BRS'),
                 datetime.datetime(2017, 10, 17, 14, 48),
                 datetime.datetime(2017, 10, 17, 15, 18) ]
        expected_result = T.Duty(
            T.TripID('13804', ''),
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
                         '201710176196~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_standard_standby(self):
        data = [
            p.DStr(datetime.date(2017, 1, 17), 'ESBY'),
            datetime.datetime(2017, 1, 17, 6, 15),
            datetime.datetime(2017, 1, 17, 14, 15)]
        expected_result = T.Duty(
            T.TripID('13531', ''),
            datetime.datetime(2017, 1, 17, 6, 15),
            datetime.datetime(2017, 1, 17, 14, 15),
            (
                T.Sector('ESBY', None, None,
                         datetime.datetime(2017, 1, 17, 6, 15),
                         datetime.datetime(2017, 1, 17, 14, 15),
                         datetime.datetime(2017, 1, 17, 6, 15),
                         datetime.datetime(2017, 1, 17, 14, 15),
                         None, None,
                         T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY,
                         None),))
        self.assertEqual(p._duty(data), expected_result)


    def test_standby_then_postioning(self):
        data = [
            p.DStr(datetime.date(2017, 10, 22), 'LSBY'),
            datetime.datetime(2017, 10, 22, 10, 0),
            datetime.datetime(2017, 10, 22, 18, 0),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 10, 22), '6140'),
            datetime.datetime(2017, 10, 22, 18, 10),
            datetime.datetime(2017, 10, 22, 19, 28),
            p.DStr(datetime.date(2017, 10, 22), '*TLS'),
            p.DStr(datetime.date(2017, 10, 22), 'BRS'),
            datetime.datetime(2017, 10, 22, 21, 25),
            datetime.datetime(2017, 10, 22, 21, 40)]
        expected_result = T.Duty(
            T.TripID('13809', ''),
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
                         '201710226140~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_return_to_stand_and_sector_across_end_of_roster(self):
        data = [
            p.DStr(datetime.date(2016, 10, 31), '6073R'),
            datetime.datetime(2016, 10, 31, 15, 30),
            datetime.datetime(2016, 10, 31, 16, 30),
            p.DStr(datetime.date(2016, 10, 31), 'BRS'),
            p.DStr(datetime.date(2016, 10, 31), 'BRS'),
            datetime.datetime(2016, 10, 31, 16, 45),
            p.Break.LINE,
            p.DStr(datetime.date(2016, 10, 31), '6073'),
            datetime.datetime(2016, 10, 31, 18, 43),
            p.DStr(datetime.date(2016, 10, 31), 'BRS'),
            p.DStr(datetime.date(2016, 10, 31), 'ALC'),
            datetime.datetime(2016, 10, 31, 21, 4),
            p.Break.LINE,
            p.DStr(datetime.date(2016, 10, 31), '6074'),
            datetime.datetime(2016, 10, 31, 21, 39),
            p.DStr(datetime.date(2016, 10, 31), 'ALC')]
        expected_result = T.Duty(
            T.TripID('13453', ''),
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
                         '201610316074~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_airport_standby_callout_and_diversion(self):
        data = [
            p.DStr(datetime.date(2016, 10, 22), 'ADTY'),
            datetime.datetime(2016, 10, 22, 5, 0),
            datetime.datetime(2016, 10, 22, 5, 0),
            datetime.datetime(2016, 10, 22, 5, 5),
            p.Break.LINE,
            p.DStr(datetime.date(2016, 10, 22), '393'),
            datetime.datetime(2016, 10, 22, 6, 7),
            p.DStr(datetime.date(2016, 10, 22), 'BRS'),
            p.DStr(datetime.date(2016, 10, 22), 'INV'),
            datetime.datetime(2016, 10, 22, 7, 35),
            p.Break.LINE,
            p.DStr(datetime.date(2016, 10, 22), '394'),
            datetime.datetime(2016, 10, 22, 8, 12),
            p.DStr(datetime.date(2016, 10, 22), 'INV'),
            p.DStr(datetime.date(2016, 10, 22), 'CWL'),
            datetime.datetime(2016, 10, 22, 9, 26),
            p.Break.LINE,
            p.DStr(datetime.date(2016, 10, 22), '394'),
            datetime.datetime(2016, 10, 22, 10, 50),
            p.DStr(datetime.date(2016, 10, 22), 'CWL'),
            p.DStr(datetime.date(2016, 10, 22), 'BRS'),
            datetime.datetime(2016, 10, 22, 11, 13),
            datetime.datetime(2016, 10, 22, 11, 43)]
        expected_result = T.Duty(
            T.TripID('13444', ''),
            datetime.datetime(2016, 10, 22, 5, 0),
            datetime.datetime(2016, 10, 22, 11, 43),
            (
                T.Sector(
                    'ADTY', None, None,
                    datetime.datetime(2016, 10, 22, 5, 0),
                    datetime.datetime(2016, 10, 22, 5, 5),
                    datetime.datetime(2016, 10, 22, 5, 0),
                    datetime.datetime(2016, 10, 22, 5, 5),
                    None, None, T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY,
                    None),
                T.Sector(
                    '393', 'BRS', 'INV',
                    datetime.datetime(2016, 10, 22, 6, 7),
                    datetime.datetime(2016, 10, 22, 7, 35),
                    datetime.datetime(2016, 10, 22, 6, 7),
                    datetime.datetime(2016, 10, 22, 7, 35),
                    None, None, T.SectorFlags.NONE,
                    '20161022393~'),
                T.Sector(
                    '394', 'INV', 'CWL',
                    datetime.datetime(2016, 10, 22, 8, 12),
                    datetime.datetime(2016, 10, 22, 9, 26),
                    datetime.datetime(2016, 10, 22, 8, 12),
                    datetime.datetime(2016, 10, 22, 9, 26),
                    None, None, T.SectorFlags.NONE,
                    '20161022394~'),
                T.Sector(
                    '394', 'CWL', 'BRS',
                    datetime.datetime(2016, 10, 22, 10, 50),
                    datetime.datetime(2016, 10, 22, 11, 13),
                    datetime.datetime(2016, 10, 22, 10, 50),
                    datetime.datetime(2016, 10, 22, 11, 13),
                    None, None, T.SectorFlags.NONE,
                    '20161022394~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_loe_with_ground_positioning(self):
        data = [
            p.DStr(datetime.date(2017, 5, 28), 'TAXI'),
            datetime.datetime(2017, 5, 28, 13, 15),
            datetime.datetime(2017, 5, 28, 13, 15),
            p.DStr(datetime.date(2017, 5, 28), '*BRS'),
            p.DStr(datetime.date(2017, 5, 28), 'XWS'),
            datetime.datetime(2017, 5, 28, 16, 45),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 5, 28), 'LOEV'),
            datetime.datetime(2017, 5, 28, 18, 15),
            datetime.datetime(2017, 5, 28, 22, 15),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 5, 28), 'TAXI'),
            datetime.datetime(2017, 5, 28, 23, 15),
            p.DStr(datetime.date(2017, 5, 28), '*XWS'),
            p.DStr(datetime.date(2017, 5, 28), 'MAN'),
            datetime.datetime(2017, 5, 28, 23, 45),
            datetime.datetime(2017, 5, 28, 23, 45)]
        expected_result = T.Duty(
            T.TripID('13662', ''),
            datetime.datetime(2017, 5, 28, 13, 15),
            datetime.datetime(2017, 5, 28, 23, 45),
            (
                T.Sector('TAXI', 'BRS', 'XWS',
                         datetime.datetime(2017, 5, 28, 13, 15),
                         datetime.datetime(2017, 5, 28, 16, 45),
                         datetime.datetime(2017, 5, 28, 13, 15),
                         datetime.datetime(2017, 5, 28, 16, 45),
                         None, None,
                         T.SectorFlags.GROUND_DUTY | T.SectorFlags.POSITIONING,
                         '20170528TAXI~'),
                T.Sector('LOEV', None, None,
                         datetime.datetime(2017, 5, 28, 18, 15),
                         datetime.datetime(2017, 5, 28, 22, 15),
                         datetime.datetime(2017, 5, 28, 18, 15),
                         datetime.datetime(2017, 5, 28, 22, 15),
                         None, None,
                         T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY,
                         None),
                T.Sector('TAXI', 'XWS', 'MAN',
                         datetime.datetime(2017, 5, 28, 23, 15),
                         datetime.datetime(2017, 5, 28, 23, 45),
                         datetime.datetime(2017, 5, 28, 23, 15),
                         datetime.datetime(2017, 5, 28, 23, 45),
                         None, None,
                         T.SectorFlags.GROUND_DUTY | T.SectorFlags.POSITIONING,
                         '20170528TAXI~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_callout_to_asby_then_callout_to_fly(self):
        data = [
            p.DStr(datetime.date(2017, 8, 6), 'LSBY'),
            datetime.datetime(2017, 8, 6, 12, 40),
            datetime.datetime(2017, 8, 6, 17, 0),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 8, 6), 'ADTY'),
            datetime.datetime(2017, 8, 6, 17, 0),
            datetime.datetime(2017, 8, 6, 17, 0),
            datetime.datetime(2017, 8, 6, 17, 45),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 8, 6), '6045'),
            datetime.datetime(2017, 8, 6, 21, 10),
            p.DStr(datetime.date(2017, 8, 6), 'BRS'),
            p.DStr(datetime.date(2017, 8, 6), 'PMI'),
            datetime.datetime(2017, 8, 6, 23, 22),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 8, 7), '6046'),
            datetime.datetime(2017, 8, 7, 0, 29),
            p.DStr(datetime.date(2017, 8, 7), 'PMI'),
            p.DStr(datetime.date(2017, 8, 7), 'BRS'),
            datetime.datetime(2017, 8, 7, 2, 46),
            datetime.datetime(2017, 8, 7, 3, 16)]
        expected_result = T.Duty(
            T.TripID('13732', ''),
            datetime.datetime(2017, 8, 6, 12, 40),
            datetime.datetime(2017, 8, 7, 3, 16),
            (
                T.Sector('LSBY', None, None,
                         datetime.datetime(2017, 8, 6, 12, 40),
                         datetime.datetime(2017, 8, 6, 17, 0),
                         datetime.datetime(2017, 8, 6, 12, 40),
                         datetime.datetime(2017, 8, 6, 17, 0),
                         None, None,
                         T.SectorFlags.QUASI| T.SectorFlags.GROUND_DUTY,
                         None),
                T.Sector('ADTY', None, None,
                         datetime.datetime(2017, 8, 6, 17, 0),
                         datetime.datetime(2017, 8, 6, 17, 45),
                         datetime.datetime(2017, 8, 6, 17, 0),
                         datetime.datetime(2017, 8, 6, 17, 45),
                         None, None,
                         T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY,
                         None),
                T.Sector('6045', 'BRS', 'PMI',
                         datetime.datetime(2017, 8, 6, 21, 10),
                         datetime.datetime(2017, 8, 6, 23, 22),
                         datetime.datetime(2017, 8, 6, 21, 10),
                         datetime.datetime(2017, 8, 6, 23, 22),
                         None, None, T.SectorFlags.NONE, '201708066045~'),
                T.Sector('6046', 'PMI', 'BRS',
                         datetime.datetime(2017, 8, 7, 0, 29),
                         datetime.datetime(2017, 8, 7, 2, 46),
                         datetime.datetime(2017, 8, 7, 0, 29),
                         datetime.datetime(2017, 8, 7, 2, 46),
                         None, None, T.SectorFlags.NONE, '201708076046~')))
        self.assertEqual(p._duty(data), expected_result)


    def test_lpc(self):
        data = [
            p.DStr(datetime.date(2019, 10, 28), 'LIPC'),
            datetime.datetime(2019, 10, 28, 17, 0),
            datetime.datetime(2019, 10, 28, 18, 30),
            datetime.datetime(2019, 10, 28, 22, 30),
            datetime.datetime(2019, 10, 28, 23, 30)]
        expected_result = T.Duty(
            T.TripID('14545', ''),
            datetime.datetime(2019, 10, 28, 17, 0),
            datetime.datetime(2019, 10, 28, 23, 30),
            (
                T.Sector(
                    'LIPC', None, None,
                    datetime.datetime(2019, 10, 28, 18, 30),
                    datetime.datetime(2019, 10, 28, 22, 30),
                    datetime.datetime(2019, 10, 28, 18, 30),
                    datetime.datetime(2019, 10, 28, 22, 30),
                    None, None,
                    T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY,
                    None),))
        self.assertEqual(p._duty(data), expected_result)


    def test_empty_stream(self):
        self.assertEqual(p._duty([]), None)


    def test_day_off(self):
        data = [p.DStr(datetime.date(2019, 10, 24), 'D/O')]
        self.assertEqual(p._duty(data), None)


    def test_bad_format_trips(self):
        data = 1 #not even a list
        with self.assertRaises(AssertionError):
            p._duty(data)

        data = [
            p.DStr(datetime.date(2017, 10, 17), '6195'),
            datetime.datetime(2017, 10, 17, 4, 30),
            datetime.datetime(2017, 10, 17, 5, 40),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            datetime.datetime(2017, 10, 17, 10, 7),
            "break", #bad break format
            p.DStr(datetime.date(2017, 10, 17), '6196'),
            datetime.datetime(2017, 10, 17, 11, 7),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            datetime.datetime(2017, 10, 17, 14, 48),
            datetime.datetime(2017, 10, 17, 15, 18) ]
        with self.assertRaises(AssertionError):
            p._duty(data)

        data = [#missing first entry
            datetime.datetime(2017, 10, 17, 4, 30),
            datetime.datetime(2017, 10, 17, 5, 40),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            datetime.datetime(2017, 10, 17, 10, 7),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 10, 17), '6196'),
            datetime.datetime(2017, 10, 17, 11, 7),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            datetime.datetime(2017, 10, 17, 14, 48),
            datetime.datetime(2017, 10, 17, 15, 18) ]
        with self.assertRaises(p.SectorFormatException):
            print(p._duty(data))

        data = [
            p.DStr(datetime.date(2017, 10, 17), '6195'),
            datetime.datetime(2017, 10, 17, 4, 30),
            datetime.datetime(2017, 10, 17, 5, 40),
            #missing from or to
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            datetime.datetime(2017, 10, 17, 10, 7),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 10, 17), '6196'),
            datetime.datetime(2017, 10, 17, 11, 7),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            datetime.datetime(2017, 10, 17, 14, 48),
            datetime.datetime(2017, 10, 17, 15, 18) ]
        with self.assertRaises(p.SectorFormatException):
            print(p._duty(data))

        data = [
            p.DStr(datetime.date(2017, 10, 17), '6195'),
            datetime.datetime(2017, 10, 17, 4, 30),
            datetime.datetime(2017, 10, 17, 5, 40),
            p.DStr(datetime.date(2017, 10, 17), 'BRS'),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            datetime.datetime(2017, 10, 17, 10, 7),
            p.Break.LINE,
            p.DStr(datetime.date(2017, 10, 17), '6196'),
            datetime.datetime(2017, 10, 17, 11, 7),
            p.DStr(datetime.date(2017, 10, 17), 'LPA'),
            p.DStr(datetime.date(2017, 10, 17), 'BRS')]
        #end data missing but wrong for midnight over last entry case
        with self.assertRaises(p.SectorFormatException):
            print(p._duty(data))
