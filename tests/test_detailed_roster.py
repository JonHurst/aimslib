#!/usr/bin/python3

import unittest
import datetime
import aimslib.detailed_roster.process as p
import aimslib.common.types as T


class Test_basic_stream(unittest.TestCase):

    def test_standard_overnights(self):
        data = [
            [
                'Oct21\nMon', 'EZS', '6245', '05:30', '06:34', 'BRS', 'FNC', '09:45', '(320)', '',
                'EJU', '6246', '10:32', 'FNC', 'BRS', '13:59', '14:29', '(320)', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [
                'Oct22\nTue', 'G\xa0EJU', '6205', '04:15', '05:12', 'BRS', 'SPU', '07:56', '(320)', '',
                '6206', '13:16', 'SPU', 'BRS', '15:50', '16:20', '(320)', 'FO', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'M', ''],
            [
                'Oct23\nWed', 'D/O', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 21), text='EZS'),
            p.DStr(date=datetime.date(2019, 10, 21), text='6245'),
            datetime.datetime(2019, 10, 21, 5, 30),
            datetime.datetime(2019, 10, 21, 6, 34),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            datetime.datetime(2019, 10, 21, 9, 45),
            p.DStr(date=datetime.date(2019, 10, 21), text='(320)'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 21), text='EJU'),
            p.DStr(date=datetime.date(2019, 10, 21), text='6246'),
            datetime.datetime(2019, 10, 21, 10, 32),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            datetime.datetime(2019, 10, 21, 13, 59),
            datetime.datetime(2019, 10, 21, 14, 29),
            p.DStr(date=datetime.date(2019, 10, 21), text='(320)'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 22), text='G\xa0EJU'),
            p.DStr(date=datetime.date(2019, 10, 22), text='6205'),
            datetime.datetime(2019, 10, 22, 4, 15),
            datetime.datetime(2019, 10, 22, 5, 12),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            datetime.datetime(2019, 10, 22, 7, 56),
            p.DStr(date=datetime.date(2019, 10, 22), text='(320)'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 22), text='6206'),
            datetime.datetime(2019, 10, 22, 13, 16),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            datetime.datetime(2019, 10, 22, 15, 50),
            datetime.datetime(2019, 10, 22, 16, 20),
            p.DStr(date=datetime.date(2019, 10, 22), text='(320)'),
            p.DStr(date=datetime.date(2019, 10, 22), text='FO'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 22), text='M'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 23), text='D/O'),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 10, 21), data),
            expected_result)


    def test_blank_column(self):
        data = [
            ['Oct31\nThu', 'D/O', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 31), text='D/O'),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 10, 31), data),
            expected_result)


    def test_extra_codes(self):
        data = [
            ['Sep11\nWed', 'l', '6189', '05:20', '06:46', 'BRS', 'PSA', '08:46', '', 'l',
             '6190', '09:22', 'PSA', 'BRS', '11:49', '12:19', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 9, 11), text='l'),
            p.DStr(date=datetime.date(2019, 9, 11), text='6189'),
            datetime.datetime(2019, 9, 11, 5, 20),
            datetime.datetime(2019, 9, 11, 6, 46),
            p.DStr(date=datetime.date(2019, 9, 11), text='BRS'),
            p.DStr(date=datetime.date(2019, 9, 11), text='PSA'),
            datetime.datetime(2019, 9, 11, 8, 46),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 9, 11), text='l'),
            p.DStr(date=datetime.date(2019, 9, 11), text='6190'),
            datetime.datetime(2019, 9, 11, 9, 22),
            p.DStr(date=datetime.date(2019, 9, 11), text='PSA'),
            p.DStr(date=datetime.date(2019, 9, 11), text='BRS'),
            datetime.datetime(2019, 9, 11, 11, 49),
            datetime.datetime(2019, 9, 11, 12, 19),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 9, 11), data),
            expected_result)


    def test_across_midnight(self):
        data = [
            [
                'May18\nSat', '6045', '17:45', '18:45', 'BRS', 'PMI', '21:00',
                '', '6046', '21:35', 'PMI', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', ''],
            [
                'May19\nSun', 'BRS', '23:55', '00:25', '', 'REST', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', ''],

            [
                'May20\nMon', 'D/O', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 18), text='6045'),
            datetime.datetime(2019, 5, 18, 17, 45),
            datetime.datetime(2019, 5, 18, 18, 45),
            p.DStr(date=datetime.date(2019, 5, 18), text='BRS'),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            datetime.datetime(2019, 5, 18, 21, 0),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 18), text='6046'),
            datetime.datetime(2019, 5, 18, 21, 35),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 19), text='BRS'),
            datetime.datetime(2019, 5, 18, 23, 55),
            datetime.datetime(2019, 5, 19, 0, 25),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 19), text='REST'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 20), text='D/O'),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 5, 18), data),
            expected_result)


    def test_lpc(self):
        data = [
            [
                'Oct27\nSun', 'TAXI', '13:45', '13:45', '*BRS', 'LGW',
                '16:30', '', 'OPCV', '18:30', '22:30', '23:30', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', ''],
            [
                'Oct28\nMon', 'LIPC', '17:00', '18:30', '22:30', '23:30',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                'M', ''],
            [
                'Oct29\nTue', 'TAXI', '10:30', '10:30', '*LGW', 'BRS',
                '13:30', '13:30', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 27), text='TAXI'),
            datetime.datetime(2019, 10, 27, 13, 45),
            datetime.datetime(2019, 10, 27, 13, 45),
            p.DStr(date=datetime.date(2019, 10, 27), text='*BRS'),
            p.DStr(date=datetime.date(2019, 10, 27), text='LGW'),
            datetime.datetime(2019, 10, 27, 16, 30),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 27), text='OPCV'),
            datetime.datetime(2019, 10, 27, 18, 30),
            datetime.datetime(2019, 10, 27, 22, 30),
            datetime.datetime(2019, 10, 27, 23, 30),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 28), text='LIPC'),
            datetime.datetime(2019, 10, 28, 17, 0),
            datetime.datetime(2019, 10, 28, 18, 30),
            datetime.datetime(2019, 10, 28, 22, 30),
            datetime.datetime(2019, 10, 28, 23, 30),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 28), text='M'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 29), text='TAXI'),
            datetime.datetime(2019, 10, 29, 10, 30),
            datetime.datetime(2019, 10, 29, 10, 30),
            p.DStr(date=datetime.date(2019, 10, 29), text='*LGW'),
            p.DStr(date=datetime.date(2019, 10, 29), text='BRS'),
            datetime.datetime(2019, 10, 29, 13, 30),
            datetime.datetime(2019, 10, 29, 13, 30),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 10, 27), data),
            expected_result)


    def test_lpc_across_midnight(self):
        data = [
            [
                'Apr28\nSun', 'LOE', '19:00', '20:30', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', ''],
            ['Apr29\nMon', '00:30', '01:30', '', '6224', '16:00', '17:00',
             '*CDG', 'BRS', '18:08', '18:23', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', 'M', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 4, 28), text='LOE'),
            datetime.datetime(2019, 4, 28, 19, 0),
            datetime.datetime(2019, 4, 28, 20, 30),
            p.Break.COLUMN,
            datetime.datetime(2019, 4, 29, 0, 30),
            datetime.datetime(2019, 4, 29, 1, 30),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 4, 29), text='6224'),
            datetime.datetime(2019, 4, 29, 16, 0),
            datetime.datetime(2019, 4, 29, 17, 0),
            p.DStr(date=datetime.date(2019, 4, 29), text='*CDG'),
            p.DStr(date=datetime.date(2019, 4, 29), text='BRS'),
            datetime.datetime(2019, 4, 29, 18, 8),
            datetime.datetime(2019, 4, 29, 18, 23),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 4, 29), text='M'),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 4, 28), data),
            expected_result)


    def test_dragover_case(self):
        data = [
            [
                'May27\nSat', '6133', '14:55', '16:01', 'BRS', 'EFL', '19:23', '', '6134', '20:00', 'EFL',
                '(320)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [
                'May28\nSun', 'BRS', '23:32', '00:02', '', 'TAXI', '13:15', '13:15', '*BRS', 'XWS', '16:45',
                '', 'LOEV', '18:15', '22:15', '', 'TAXI', '23:15', '*XWS', 'MAN', '23:45', '23:45', '', '', '',
                '', '', '', '', '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2017, 5, 27), text='6133'),
            datetime.datetime(2017, 5, 27, 14, 55),
            datetime.datetime(2017, 5, 27, 16, 1),
            p.DStr(date=datetime.date(2017, 5, 27), text='BRS'),
            p.DStr(date=datetime.date(2017, 5, 27), text='EFL'),
            datetime.datetime(2017, 5, 27, 19, 23),
            p.Break.LINE,
            p.DStr(date=datetime.date(2017, 5, 27), text='6134'),
            datetime.datetime(2017, 5, 27, 20, 0),
            p.DStr(date=datetime.date(2017, 5, 27), text='EFL'),
            p.DStr(date=datetime.date(2017, 5, 27), text='(320)'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2017, 5, 28), text='BRS'),
            datetime.datetime(2017, 5, 27, 23, 32), #Tricksy bit
            datetime.datetime(2017, 5, 28, 0, 2),
            p.Break.LINE,
            p.DStr(date=datetime.date(2017, 5, 28), text='TAXI'),
            datetime.datetime(2017, 5, 28, 13, 15),
            datetime.datetime(2017, 5, 28, 13, 15),
            p.DStr(date=datetime.date(2017, 5, 28), text='*BRS'),
            p.DStr(date=datetime.date(2017, 5, 28), text='XWS'),
            datetime.datetime(2017, 5, 28, 16, 45),
            p.Break.LINE,
            p.DStr(date=datetime.date(2017, 5, 28), text='LOEV'),
            datetime.datetime(2017, 5, 28, 18, 15),
            datetime.datetime(2017, 5, 28, 22, 15),
            p.Break.LINE,
            p.DStr(date=datetime.date(2017, 5, 28), text='TAXI'),
            datetime.datetime(2017, 5, 28, 23, 15),
            p.DStr(date=datetime.date(2017, 5, 28), text='*XWS'),
            p.DStr(date=datetime.date(2017, 5, 28), text='MAN'),
            datetime.datetime(2017, 5, 28, 23, 45),
            datetime.datetime(2017, 5, 28, 23, 45),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2017, 5, 27), data),
            expected_result)


    def test_2400_bug(self):
        data = [
            [
                'May17\nFri', '6001', '16:50', '17:50', 'BRS', 'FAO', '20:25', '(320)', '',
                '6002', '20:55', 'FAO', 'BRS', '23:30', '24:00', '(320)', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 17), text='6001'),
            datetime.datetime(2019, 5, 17, 16, 50),
            datetime.datetime(2019, 5, 17, 17, 50),
            p.DStr(date=datetime.date(2019, 5, 17), text='BRS'),
            p.DStr(date=datetime.date(2019, 5, 17), text='FAO'),
            datetime.datetime(2019, 5, 17, 20, 25),
            p.DStr(date=datetime.date(2019, 5, 17), text='(320)'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 17), text='6002'),
            datetime.datetime(2019, 5, 17, 20, 55),
            p.DStr(date=datetime.date(2019, 5, 17), text='FAO'),
            p.DStr(date=datetime.date(2019, 5, 17), text='BRS'),
            datetime.datetime(2019, 5, 17, 23, 30),
            datetime.datetime(2019, 5, 18, 0, 0), #tricksy bit
            p.DStr(date=datetime.date(2019, 5, 17), text='(320)'),
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 5, 17), data),
            expected_result)


    def test_bad_input_formats(self):
        with self.assertRaises(AssertionError):
            p.basic_stream(None, [[]])
        with self.assertRaises(AssertionError):
            p.basic_stream("bad", [[]])
        with self.assertRaises(AssertionError):
            p.basic_stream(datetime.date(2019, 1, 1), None)
        with self.assertRaises(AssertionError):
            p.basic_stream(datetime.date(2019, 1, 1), [1, 2])
        with self.assertRaises(AssertionError):
            p.basic_stream(datetime.date(2019, 1, 1), [["AAA", "BBB", 1]])


    def test_bad_time(self):
        """Bad times should be tagged as strings"""
        data = [
            [
                'May17\nFri', '6001', '16:50', '17:50', 'BRS', 'FAO',
                '20:25', '24:30']]
        expected_result = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 17), text='6001'),
            datetime.datetime(2019, 5, 17, 16, 50),
            datetime.datetime(2019, 5, 17, 17, 50),
            p.DStr(date=datetime.date(2019, 5, 17), text='BRS'),
            p.DStr(date=datetime.date(2019, 5, 17), text='FAO'),
            datetime.datetime(2019, 5, 17, 20, 25),
            p.DStr(date=datetime.date(2019, 5, 17), text='24:30'), #tricksy
            p.Break.COLUMN]
        self.assertEqual(
            p.basic_stream(datetime.date(2019, 5, 17), data),
            expected_result)



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


class TestDutyStream(unittest.TestCase):

    def test_standard(self):
        data = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 21), text='l'),
            p.DStr(date=datetime.date(2019, 10, 21), text='EJU'),
            p.DStr(date=datetime.date(2019, 10, 21), text='6245'),
            datetime.datetime(2019, 10, 21, 5, 30),
            datetime.datetime(2019, 10, 21, 6, 34),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            datetime.datetime(2019, 10, 21, 9, 45),
            p.DStr(date=datetime.date(2019, 10, 21), text='(320)'),
            p.DStr(date=datetime.date(2019, 10, 21), text='FO'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 21), text='M'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 21), text='6246'),
            datetime.datetime(2019, 10, 21, 10, 32),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            datetime.datetime(2019, 10, 21, 13, 59),
            datetime.datetime(2019, 10, 21, 14, 29),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 22), text='6205'),
            datetime.datetime(2019, 10, 22, 4, 15),
            datetime.datetime(2019, 10, 22, 5, 12),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            datetime.datetime(2019, 10, 22, 7, 56),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 22), text='6206'),
            datetime.datetime(2019, 10, 22, 13, 16),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            datetime.datetime(2019, 10, 22, 15, 50),
            datetime.datetime(2019, 10, 22, 16, 20),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 23), text='D/O'),
            p.Break.COLUMN]
        expected_result = [
            p.DStr(date=datetime.date(2019, 10, 21), text='6245'),
            datetime.datetime(2019, 10, 21, 5, 30),
            datetime.datetime(2019, 10, 21, 6, 34),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            datetime.datetime(2019, 10, 21, 9, 45),
            p.Break.SECTOR,
            p.DStr(date=datetime.date(2019, 10, 21), text='6246'),
            datetime.datetime(2019, 10, 21, 10, 32),
            p.DStr(date=datetime.date(2019, 10, 21), text='FNC'),
            p.DStr(date=datetime.date(2019, 10, 21), text='BRS'),
            datetime.datetime(2019, 10, 21, 13, 59),
            datetime.datetime(2019, 10, 21, 14, 29),
            p.Break.DUTY,
            p.DStr(date=datetime.date(2019, 10, 22), text='6205'),
            datetime.datetime(2019, 10, 22, 4, 15),
            datetime.datetime(2019, 10, 22, 5, 12),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            datetime.datetime(2019, 10, 22, 7, 56),
            p.Break.SECTOR,
            p.DStr(date=datetime.date(2019, 10, 22), text='6206'),
            datetime.datetime(2019, 10, 22, 13, 16),
            p.DStr(date=datetime.date(2019, 10, 22), text='SPU'),
            p.DStr(date=datetime.date(2019, 10, 22), text='BRS'),
            datetime.datetime(2019, 10, 22, 15, 50),
            datetime.datetime(2019, 10, 22, 16, 20),]
        self.assertEqual(p.duty_stream(data), expected_result)


    def test_across_midnight(self):
        data = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 18), text='6045'),
            datetime.datetime(2019, 5, 18, 17, 45),
            datetime.datetime(2019, 5, 18, 18, 45),
            p.DStr(date=datetime.date(2019, 5, 18), text='BRS'),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            datetime.datetime(2019, 5, 18, 21, 0),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 18), text='6046'),
            datetime.datetime(2019, 5, 18, 21, 35),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            p.DStr(date=datetime.date(2019, 5, 18), text='(320)'),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 18), text='M'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 19), text='BRS'),
            datetime.datetime(2019, 5, 18, 23, 55),
            datetime.datetime(2019, 5, 19, 0, 25),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 5, 19), text='REST'),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 5, 20), text='D/O'),
            p.Break.COLUMN]
        expected_result = [
            p.DStr(date=datetime.date(2019, 5, 18), text='6045'),
            datetime.datetime(2019, 5, 18, 17, 45),
            datetime.datetime(2019, 5, 18, 18, 45),
            p.DStr(date=datetime.date(2019, 5, 18), text='BRS'),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            datetime.datetime(2019, 5, 18, 21, 0),
            p.Break.SECTOR,
            p.DStr(date=datetime.date(2019, 5, 18), text='6046'),
            datetime.datetime(2019, 5, 18, 21, 35),
            p.DStr(date=datetime.date(2019, 5, 18), text='PMI'),
            p.DStr(date=datetime.date(2019, 5, 19), text='BRS'),
            datetime.datetime(2019, 5, 18, 23, 55),
            datetime.datetime(2019, 5, 19, 0, 25),]
        self.assertEqual(p.duty_stream(data), expected_result)


    def test_lpc(self):
        data = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 27), text='TAXI'),
            datetime.datetime(2019, 10, 27, 13, 45),
            datetime.datetime(2019, 10, 27, 13, 45),
            p.DStr(date=datetime.date(2019, 10, 27), text='*BRS'),
            p.DStr(date=datetime.date(2019, 10, 27), text='LGW'),
            datetime.datetime(2019, 10, 27, 16, 30),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 10, 27), text='OPCV'),
            datetime.datetime(2019, 10, 27, 18, 30),
            datetime.datetime(2019, 10, 27, 22, 30),
            datetime.datetime(2019, 10, 27, 23, 30),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 28), text='LIPC'),
            datetime.datetime(2019, 10, 28, 17, 0),
            datetime.datetime(2019, 10, 28, 18, 30),
            datetime.datetime(2019, 10, 28, 22, 30),
            datetime.datetime(2019, 10, 28, 23, 30),
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 10, 29), text='TAXI'),
            datetime.datetime(2019, 10, 29, 10, 30),
            datetime.datetime(2019, 10, 29, 10, 30),
            p.DStr(date=datetime.date(2019, 10, 29), text='*LGW'),
            p.DStr(date=datetime.date(2019, 10, 29), text='BRS'),
            datetime.datetime(2019, 10, 29, 13, 30),
            datetime.datetime(2019, 10, 29, 13, 30),
            p.Break.COLUMN]
        expected_result = [
            p.DStr(date=datetime.date(2019, 10, 27), text='TAXI'),
            datetime.datetime(2019, 10, 27, 13, 45),
            datetime.datetime(2019, 10, 27, 13, 45),
            p.DStr(date=datetime.date(2019, 10, 27), text='*BRS'),
            p.DStr(date=datetime.date(2019, 10, 27), text='LGW'),
            datetime.datetime(2019, 10, 27, 16, 30),
            p.Break.SECTOR,
            p.DStr(date=datetime.date(2019, 10, 27), text='OPCV'),
            datetime.datetime(2019, 10, 27, 18, 30),
            datetime.datetime(2019, 10, 27, 22, 30),
            datetime.datetime(2019, 10, 27, 23, 30),
            p.Break.DUTY,
            p.DStr(date=datetime.date(2019, 10, 28), text='LIPC'),
            datetime.datetime(2019, 10, 28, 17, 0),
            datetime.datetime(2019, 10, 28, 18, 30),
            datetime.datetime(2019, 10, 28, 22, 30),
            datetime.datetime(2019, 10, 28, 23, 30),
            p.Break.DUTY,
            p.DStr(date=datetime.date(2019, 10, 29), text='TAXI'),
            datetime.datetime(2019, 10, 29, 10, 30),
            datetime.datetime(2019, 10, 29, 10, 30),
            p.DStr(date=datetime.date(2019, 10, 29), text='*LGW'),
            p.DStr(date=datetime.date(2019, 10, 29), text='BRS'),
            datetime.datetime(2019, 10, 29, 13, 30),
            datetime.datetime(2019, 10, 29, 13, 30)]
        self.assertEqual(p.duty_stream(data), expected_result)


    def test_lpc_over_midnight(self):
        data = [
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 4, 28), text='LOE'),
            datetime.datetime(2019, 4, 28, 19, 0),
            datetime.datetime(2019, 4, 28, 20, 30),
            p.Break.COLUMN,
            datetime.datetime(2019, 4, 29, 0, 30),
            datetime.datetime(2019, 4, 29, 1, 30),
            p.Break.LINE,
            p.DStr(date=datetime.date(2019, 4, 29), text='6224'),
            datetime.datetime(2019, 4, 29, 16, 0),
            datetime.datetime(2019, 4, 29, 17, 0),
            p.DStr(date=datetime.date(2019, 4, 29), text='*CDG'),
            p.DStr(date=datetime.date(2019, 4, 29), text='BRS'),
            datetime.datetime(2019, 4, 29, 18, 8),
            datetime.datetime(2019, 4, 29, 18, 23),
            p.Break.COLUMN]
        expected_result = [
            p.DStr(date=datetime.date(2019, 4, 28), text='LOE'),
            datetime.datetime(2019, 4, 28, 19, 0),
            datetime.datetime(2019, 4, 28, 20, 30),
            datetime.datetime(2019, 4, 29, 0, 30),
            datetime.datetime(2019, 4, 29, 1, 30),
            p.Break.DUTY,
            p.DStr(date=datetime.date(2019, 4, 29), text='6224'),
            datetime.datetime(2019, 4, 29, 16, 0),
            datetime.datetime(2019, 4, 29, 17, 0),
            p.DStr(date=datetime.date(2019, 4, 29), text='*CDG'),
            p.DStr(date=datetime.date(2019, 4, 29), text='BRS'),
            datetime.datetime(2019, 4, 29, 18, 8),
            datetime.datetime(2019, 4, 29, 18, 23)]
        self.assertEqual(p.duty_stream(data), expected_result)


    def test_badstream(self):
        with self.assertRaises(AssertionError):
            p.duty_stream(None)
        with self.assertRaises(AssertionError):
            p.duty_stream("string")
        with self.assertRaises(AssertionError):
            p.duty_stream(["string1", "string2"])
        data = [#random segment
            datetime.datetime(2019, 4, 28, 20, 30),
            p.Break.COLUMN,
            datetime.datetime(2019, 4, 29, 0, 30)
            ]
        with self.assertRaises(AssertionError):
            p.duty_stream(data)
        data = [#dstream
            p.DStr(date=datetime.date(2019, 4, 28), text='LOE'),
            datetime.datetime(2019, 4, 28, 19, 0),
            datetime.datetime(2019, 4, 28, 20, 30),
            datetime.datetime(2019, 4, 29, 0, 30),
            datetime.datetime(2019, 4, 29, 1, 30),
            p.Break.DUTY,
            p.DStr(date=datetime.date(2019, 4, 29), text='6224'),
            datetime.datetime(2019, 4, 29, 16, 0),
            datetime.datetime(2019, 4, 29, 17, 0),
            p.DStr(date=datetime.date(2019, 4, 29), text='*CDG'),
            p.DStr(date=datetime.date(2019, 4, 29), text='BRS'),
            datetime.datetime(2019, 4, 29, 18, 8),
            datetime.datetime(2019, 4, 29, 18, 23)]
        with self.assertRaises(AssertionError):
            p.duty_stream(data)
        data = [
            p.Break.COLUMN,
            p.Break.COLUMN,
            p.DStr(date=datetime.date(2019, 4, 28), text='LOE'),
            datetime.datetime(2019, 4, 28, 19, 0),
            p.Break.COLUMN]
        with self.assertRaises(p.SectorFormatException):
            p.duty_stream(data)


class TestCrew(unittest.TestCase):

    def setUp(self):
        self.oldfunc = p._crew_strings
        def fake_crew_strings(_):
            return self.test_crew_strings
        p._crew_strings = fake_crew_strings


    def tearDown(self):
        p._crew_strings = self.oldfunc


    def test_standard(self):
        self.test_crew_strings = [
'09/04/2019 All               FO> HUTTON STUART       PU> WELCH FIONA         FA> CALLACHAN MICHAEL   FA> HAWKINGS KERRIN     FA> LUCAS BETHANY      ',
'                             FA> LINE EXTRA',
'10/04/2019 569,570,6253,6254 FO> VINCENT RICHARD     PU> SIMS GEORGIA        FA> DOUGLAS AYSHA       FA> KIMBERLEY CHRISTOPH FA> VINCENT  LORNA     ',
'10/04/2019 *6253             CP> RIDLEY LEON SR     ',
'10/04/2019 *6254             PU> PEACEY EMMA        ',
'11/04/2019 All               FO> VINCENT RICHARD     PU> SHARRATT CHRISTOPHE FA> KIMBERLEY CHRISTOPH FA> LEWIS ANNA          FA> MADDEN CHLOE       ',
            ]
        duties = [
    T.Duty(
        T.TripID('14343', ''),
        datetime.datetime(2019, 4, 9, 15, 30),
        datetime.datetime(2019, 4, 9, 22, 33),
        (
            T.Sector('6073', 'BRS', 'ALC',
                   datetime.datetime(2019, 4, 9, 16, 27),
                   datetime.datetime(2019, 4, 9, 18, 55),
                   datetime.datetime(2019, 4, 9, 16, 27),
                   datetime.datetime(2019, 4, 9, 18, 55),
                   None, None, T.SectorFlags.NONE, '201904096073~'),
            T.Sector('6074', 'ALC', 'BRS',
                   datetime.datetime(2019, 4, 9, 19, 37),
                   datetime.datetime(2019, 4, 9, 22, 3),
                   datetime.datetime(2019, 4, 9, 19, 37),
                   datetime.datetime(2019, 4, 9, 22, 3),
                   None, None, T.SectorFlags.NONE, '201904096074~'))),
    T.Duty(
        T.TripID('14344', ''),
        datetime.datetime(2019, 4, 10, 11, 45),
        datetime.datetime(2019, 4, 10, 22, 6),
        (
            T.Sector('6253', 'BRS', 'LIS',
                     datetime.datetime(2019, 4, 10, 13, 11),
                     datetime.datetime(2019, 4, 10, 15, 28),
                     datetime.datetime(2019, 4, 10, 13, 11),
                     datetime.datetime(2019, 4, 10, 15, 28),
                     None, None, T.SectorFlags.NONE, '201904106253~'),
            T.Sector('6254', 'LIS', 'BRS',
                     datetime.datetime(2019, 4, 10, 16, 17),
                     datetime.datetime(2019, 4, 10, 18, 45),
                     datetime.datetime(2019, 4, 10, 16, 17),
                     datetime.datetime(2019, 4, 10, 18, 45),
                     None, None, T.SectorFlags, '201904106254~'),
            T.Sector('570', 'BRS', 'NCL',
                     datetime.datetime(2019, 4, 10, 19, 12),
                     datetime.datetime(2019, 4, 10, 20, 13),
                     datetime.datetime(2019, 4, 10, 19, 12),
                     datetime.datetime(2019, 4, 10, 20, 13),
                     None, None, T.SectorFlags.NONE, '20190410570~'),
            T.Sector('569', 'NCL', 'BRS',
                     datetime.datetime(2019, 4, 10, 20, 38),
                     datetime.datetime(2019, 4, 10, 21, 36),
                     datetime.datetime(2019, 4, 10, 20, 38),
                     datetime.datetime(2019, 4, 10, 21, 36),
                     None, None, T.SectorFlags.NONE, '20190410569~'))),
    T.Duty(
        T.TripID('14345', ''),
        datetime.datetime(2019, 4, 11, 11, 20),
        datetime.datetime(2019, 4, 11, 22, 20),
        (
            T.Sector('6241', 'BRS', 'BIO',
                     datetime.datetime(2019, 4, 11, 12, 15),
                     datetime.datetime(2019, 4, 11, 13, 54),
                     datetime.datetime(2019, 4, 11, 12, 15),
                     datetime.datetime(2019, 4, 11, 13, 54),
                     None, None, T.SectorFlags.NONE, '201904116241~'),
            T.Sector('6242', 'BIO', 'BRS',
                     datetime.datetime(2019, 4, 11, 14, 46),
                     datetime.datetime(2019, 4, 11, 16, 22),
                     datetime.datetime(2019, 4, 11, 14, 46),
                     datetime.datetime(2019, 4, 11, 16, 22),
                     None, None, T.SectorFlags.NONE, '201904116242~'),
            T.Sector('6035', 'BRS', 'MAD',
                     datetime.datetime(2019, 4, 11, 17, 0),
                     datetime.datetime(2019, 4, 11, 19, 6),
                     datetime.datetime(2019, 4, 11, 17, 0),
                     datetime.datetime(2019, 4, 11, 19, 6),
                     None, None, T.SectorFlags.NONE, '201904116035~'),
            T.Sector('6036', 'MAD', 'BRS',
                     datetime.datetime(2019, 4, 11, 19, 44),
                     datetime.datetime(2019, 4, 11, 21, 50),
                     datetime.datetime(2019, 4, 11, 19, 44),
                     datetime.datetime(2019, 4, 11, 21, 50),
                     None, None, T.SectorFlags.NONE, '201904116036~')))
        ]
        expected_results = {
            '201904096073~': (T.CrewMember("Hutton Stuart", "FO"),
                              T.CrewMember("Welch Fiona", "PU"),
                              T.CrewMember("Callachan Michael", "FA"),
                              T.CrewMember("Hawkings Kerrin", "FA"),
                              T.CrewMember("Lucas Bethany", "FA"),
                              T.CrewMember("Line Extra", "FA")),
            '201904096074~': (T.CrewMember("Hutton Stuart", "FO"),
                              T.CrewMember("Welch Fiona", "PU"),
                              T.CrewMember("Callachan Michael", "FA"),
                              T.CrewMember("Hawkings Kerrin", "FA"),
                              T.CrewMember("Lucas Bethany", "FA"),
                              T.CrewMember("Line Extra", "FA")),
            '20190410569~': (T.CrewMember("Vincent Richard", "FO"),
                             T.CrewMember("Sims Georgia", "PU"),
                             T.CrewMember("Douglas Aysha", "FA"),
                             T.CrewMember("Kimberley Christoph", "FA"),
                             T.CrewMember("Vincent Lorna", "FA")),
            '20190410570~': (T.CrewMember("Vincent Richard", "FO"),
                             T.CrewMember("Sims Georgia", "PU"),
                             T.CrewMember("Douglas Aysha", "FA"),
                             T.CrewMember("Kimberley Christoph", "FA"),
                             T.CrewMember("Vincent Lorna", "FA")),
            '201904106253~': (T.CrewMember("Vincent Richard", "FO"),
                             T.CrewMember("Sims Georgia", "PU"),
                             T.CrewMember("Douglas Aysha", "FA"),
                             T.CrewMember("Kimberley Christoph", "FA"),
                             T.CrewMember("Vincent Lorna", "FA")),
            '201904106254~': (T.CrewMember("Vincent Richard", "FO"),
                             T.CrewMember("Sims Georgia", "PU"),
                             T.CrewMember("Douglas Aysha", "FA"),
                             T.CrewMember("Kimberley Christoph", "FA"),
                             T.CrewMember("Vincent Lorna", "FA")),
            '20190410*6253~': (T.CrewMember("Ridley Leon Sr", "CP"),),
            '20190410*6254~': (T.CrewMember("Peacey Emma", "PU"),),
            '201904116241~': (T.CrewMember("Vincent Richard", "FO"),
                              T.CrewMember("Sharratt Christophe", "PU"),
                              T.CrewMember("Kimberley Christoph", "FA"),
                              T.CrewMember("Lewis Anna", "FA"),
                              T.CrewMember("Madden Chloe", "FA")),
            '201904116242~': (T.CrewMember("Vincent Richard", "FO"),
                              T.CrewMember("Sharratt Christophe", "PU"),
                              T.CrewMember("Kimberley Christoph", "FA"),
                              T.CrewMember("Lewis Anna", "FA"),
                              T.CrewMember("Madden Chloe", "FA")),
            '201904116035~': (T.CrewMember("Vincent Richard", "FO"),
                              T.CrewMember("Sharratt Christophe", "PU"),
                              T.CrewMember("Kimberley Christoph", "FA"),
                              T.CrewMember("Lewis Anna", "FA"),
                              T.CrewMember("Madden Chloe", "FA")),
            '201904116036~': (T.CrewMember("Vincent Richard", "FO"),
                              T.CrewMember("Sharratt Christophe", "PU"),
                              T.CrewMember("Kimberley Christoph", "FA"),
                              T.CrewMember("Lewis Anna", "FA"),
                              T.CrewMember("Madden Chloe", "FA"))
        }
        self.assertEqual(p.crew("", duties), expected_results)


    def test_no_crewtable_or_duties(self):
        self.test_crew_strings = []
        self.assertEqual(p.crew("", []), {})


    def test_bad_crewstrings(self):
        self.test_crew_strings = ['10/04/2019 569,570,6253,6254 FO>']
        with self.assertRaises(p.CrewFormatException):
            p.crew("", [])
        self.test_crew_strings = ['09/04/2019 FO> HUTTON STUART']
        with self.assertRaises(p.CrewFormatException):
            p.crew("", [])
        self.test_crew_strings = ['31/11/2019 All   FO> HUTTON STUART']
        with self.assertRaises(p.CrewFormatException):
            p.crew("", [])
