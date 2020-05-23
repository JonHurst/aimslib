import unittest
import datetime as dt

import aimslib.access.trip as Trip
from aimslib.common.types import (
    Sector, SectorFlags,
    BadTripDetails
)

class TestTripParsing(unittest.TestCase):

    def test_trip_parse(self):
        html = "<html><body><table>{}</table><body></html>".format(
"""
<tr class="mono_rows_ctrl_f3">
<td>LSBY BRS BRS 0600 0910 Fri18Jan 1 09:10 09:10 06:00 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14262,138549409849,14262,401,brs,1, ,gla,320">
<td>401  BRS GLA 0855 1010 A0900 A1009 OE-IVK 1:09 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14262,138549409849,14262,402,gla,1, ,brs,320">
<td>402 GLA BRS 1035 1145 A1040 A1145 OE-IVK 1:05 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14262,138549409849,14262,6085,brs,1, ,bsl,320">
<td>6085 BRS BSL 1215 1350 A1216 A1356 OE-IVK 1:40 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14262,138549409849,14262,6086,bsl,1, ,brs,320">
<td>6086 BSL BRS 1415 1600 A1425 A1603 OE-IVK 1:38 16:03 16:03 16:33 </td></tr>
""")
        dutylist = Trip.parse(html)
        self.assertEqual(dutylist, [
            [
                [None,
                 'LSBY', 'BRS', 'BRS', '0600', '0910', 'Fri18Jan', '1',
                 '09:10', '09:10', '06:00'],
                ['14262,138549409849,14262,401,brs,1, ,gla,320',
                 '401', 'BRS', 'GLA', '0855', '1010',
                 'A0900', 'A1009', 'OE-IVK', '1:09'],
                ['14262,138549409849,14262,402,gla,1, ,brs,320',
                 '402', 'GLA', 'BRS', '1035', '1145',
                 'A1040', 'A1145', 'OE-IVK', '1:05'],
                ['14262,138549409849,14262,6085,brs,1, ,bsl,320',
                 '6085', 'BRS', 'BSL', '1215', '1350',
                 'A1216', 'A1356', 'OE-IVK', '1:40'],
                ['14262,138549409849,14262,6086,bsl,1, ,brs,320',
                 '6086', 'BSL', 'BRS', '1415', '1600',
                 'A1425', 'A1603', 'OE-IVK', '1:38',
                 '16:03', '16:03', '16:33']]])


    def test_trip_parsing_mulitday(self):
        data = """\
<html><body><table>
<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14293,209,brs,8, ,lgw,">
<td>TAXI209 BRS LGW 0435 0820 Mon18Feb 1 PAX 4:35 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14293,8495,lgw,1, ,opo,319">
<td>8495 LGW OPO 0935 1200 PAX G-EZBC 12:15 </td></tr>

<tr class="sub_table_header_blue_courier">
<td> 17:00 Rest OPERATIONAL HOTEL 7:40 </td></tr>
<tr class="sub_table_header_blue_courier">
<td> (18/02/19 12:35) </td></tr>

<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14294,7585,opo,1, ,fnc,320">
<td>7585 OPO FNC 0615 0820 Tue19Feb 2 G-UZHP 2:05 5:15 5:15 5:15 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14294,7586,fnc,1, ,opo,320">
<td>7586 FNC OPO 0850 1050 G-UZHP 2:00 10:50 10:50 11:20 </td></tr>

<tr class="sub_table_header_blue_courier">
<td> 24:15 Rest OPERATIONAL HOTEL 4:05 OPO B 5:35 10:45 6:05 </td></tr>
<tr class="sub_table_header_blue_courier">
<td> (19/02/19 11:40) </td></tr>

<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14295,8496,opo,1, ,lgw,319">
<td>8496 OPO LGW 1235 1450 Wed20Feb 3 PAX G-EZDL 11:35 </td></tr>
<tr class="mono_rows_ctrl_f3" id="14293,353365012537,14295,209,lgw,8, ,brs,">
<td>TAXI209 LGW BRS 1505 1805 PAX 18:05 </td></tr>
</table></body></html>
"""
        dutylist = Trip.parse(data)
        self.assertEqual(dutylist, [
            [
                ['14293,353365012537,14293,209,brs,8, ,lgw,',
                 'TAXI209', 'BRS', 'LGW', '0435', '0820', 'Mon18Feb', '1',
                 'PAX', '4:35'],
                ['14293,353365012537,14293,8495,lgw,1, ,opo,319',
                 '8495', 'LGW', 'OPO', '0935', '1200',
                 'PAX', 'G-EZBC', '12:15']
            ],
            [
                ['14293,353365012537,14294,7585,opo,1, ,fnc,320',
                 '7585', 'OPO', 'FNC', '0615', '0820', 'Tue19Feb', '2',
                 'G-UZHP', '2:05', '5:15', '5:15', '5:15'],
                ['14293,353365012537,14294,7586,fnc,1, ,opo,320',
                 '7586', 'FNC', 'OPO', '0850', '1050',
                 'G-UZHP', '2:00', '10:50', '10:50', '11:20']
            ],
            [
                ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                 '8496', 'OPO', 'LGW', '1235', '1450', 'Wed20Feb', '3',
                 'PAX', 'G-EZDL', '11:35'],
                ['14293,353365012537,14295,209,lgw,8, ,brs,',
                 'TAXI209', 'LGW', 'BRS', '1505', '1805',
                 'PAX', '18:05']
            ]])

#note: a bug appears to have been introduced into AIMS where multi-day trips
# have "1" as the trip day for all days. The above test is still valid
# though.

    def test_bad_trip_details(self):
        with self.assertRaises(BadTripDetails) as cm:
            Trip.parse("Not even html")
        self.assertEqual(cm.exception.str_,
                         "tr.mono_rows_ctrl_f3 not found")
        with self.assertRaises(BadTripDetails) as cm:
            Trip.parse(
                "<html><body>"
                "<table><tr><td>Not right</td></tr></table>"
                "</body></html>")


class TestSectorProcessing(unittest.TestCase):

    def test_flight_sector_future(self):
        data = ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                '8496', 'OPO', 'LGW', '1235', '1450', 'Wed20Feb', '1',
                'G-EZDL', '11:35']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('8496', 'OPO', 'LGW',
                   dt.datetime(2000, 1, 1, 12, 35),
                   dt.datetime(2000, 1, 1, 14, 50),
                   None, None,
                   'G-EZDL', None,
                   SectorFlags.NONE,
                   '14293,353365012537,14295,8496,opo,1, ,lgw,319'))


    def test_flight_sector_over_midnight(self):
        data = ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                '8496', 'OPO', 'LGW', '2300', '0030+1', 'Wed20Feb', '1',
                'A2300', 'A0035', 'G-EZDL', '11:35']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('8496', 'OPO', 'LGW',
                   dt.datetime(2000, 1, 1, 23, 0),
                   dt.datetime(2000, 1, 2, 0, 30),
                   dt.datetime(2000, 1, 1, 23, 0),
                   dt.datetime(2000, 1, 2, 0, 35),
                   'G-EZDL', None,
                   SectorFlags.NONE,
                   '14293,353365012537,14295,8496,opo,1, ,lgw,319'))


    def test_flight_sector_over_midnight_future(self):
        data = ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                '8496', 'OPO', 'LGW', '2300', '0030+1', 'Wed20Feb', '1',
                'G-EZDL', '11:35']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('8496', 'OPO', 'LGW',
                   dt.datetime(2000, 1, 1, 23, 0),
                   dt.datetime(2000, 1, 2, 0, 30),
                   None, None,
                   'G-EZDL', None,
                   SectorFlags.NONE,
                   '14293,353365012537,14295,8496,opo,1, ,lgw,319'))


    def test_air_positioning_future(self):
        data = ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                '8496', 'OPO', 'LGW', '1235', '1450', 'Wed20Feb', '3',
                'PAX', 'G-EZDL', '11:35']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('8496', 'OPO', 'LGW',
                   dt.datetime(2000, 1, 1, 12, 35),
                   dt.datetime(2000, 1, 1, 14, 50),
                   None, None,
                   'G-EZDL', None,
                   SectorFlags.POSITIONING,
                   '14293,353365012537,14295,8496,opo,1, ,lgw,319'))


    def test_air_positioning_past(self):
        data = ['14293,353365012537,14295,8496,opo,1, ,lgw,319',
                '8496', 'OPO', 'LGW', '1235', '1450', 'Wed20Feb', '3',
                'PAX', 'A1230', 'A1445', 'G-EZDL', '11:35']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('8496', 'OPO', 'LGW',
                   dt.datetime(2000, 1, 1, 12, 35),
                   dt.datetime(2000, 1, 1, 14, 50),
                   dt.datetime(2000, 1, 1, 12, 30),
                   dt.datetime(2000, 1, 1, 14, 45),
                   'G-EZDL', None,
                   SectorFlags.POSITIONING,
                   '14293,353365012537,14295,8496,opo,1, ,lgw,319'))


    def test_ground_positioning(self):
        pass #need an example of this


    def test_quasi_sector(self):
        data = [None,
                'LSBY', 'BRS', 'BRS', '0600', '0910', 'Fri18Jan', '1',
                '09:10', '09:10', '06:00']
        result = Trip._sector(data, dt.date(2000, 1, 1))
        self.assertEqual(
            result,
            Sector('LSBY', 'BRS', 'BRS',
                   dt.datetime(2000, 1, 1, 6, 0),
                   dt.datetime(2000, 1, 1, 9, 10),
                   None, None,
                   None, None,
                   SectorFlags.QUASI| SectorFlags.GROUND_DUTY,
                   None))
