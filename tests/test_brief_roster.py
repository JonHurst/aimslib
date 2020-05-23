#!/usr/bin/python3

import datetime
import unittest
from aimslib.access.brief_roster import (
    RosterEntry,
    parse, duties,
    BadBriefRoster,
    BadRosterEntry,
)
from aimslib.common.types import Duty, TripID, Sector, SectorFlags


class TestBriefRosterParsing(unittest.TestCase):

    def test_brief_roster_parse(self):
        data = """\
<html><head></head><body><div id="main_div">

<div id="myday_14146"><table class="duties_table">
<tr><td>CSBE</td><td>3:00</td></tr>
<tr><td>&nbsp;</td><td>5:00</td></tr>
<tr><td>B006D</td><td></td></tr>
</table></div>

<div id="myday_14147"><table class="duties_table">
<tr><td>B086</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
</table></div>

<div id="myday_14150"><table class="duties_table">
<tr><td>D/O</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
</table></div>

<div id="myday_14153"><table class="duties_table">
<tr><td>LVE</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
</table></div>

<div id="myday_14157"><table class="duties_table">
<tr><td>==&gt;</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
<tr><td>B253</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
</table></div>

<div id="myday_14162"><table class="duties_table">
<tr><td>ADTY</td><td>5:00</td></tr>
<tr><td>&nbsp;</td><td>11:00</td></tr>
</table></div>

<div id="myday_14174"><table class="duties_table">
<tr><td>FTGD</td><td></td></tr>
</table></div>

<div id="myday_13869"><table class="duties_table">
<tr><td>FIRE</td><td>8:00</td></tr>
<tr><td>&nbsp;</td><td>9:30</td></tr>
<tr><td>DOOR</td><td>9:30</td></tr>
<tr><td>&nbsp;</td><td>10:45</td></tr>
<tr><td>G/S</td><td>10:45</td></tr>
<tr><td>&nbsp;</td><td>11:30</td></tr>
<tr><td>ASEC</td><td>11:30</td></tr>
<tr><td>&nbsp;</td><td>13:00</td></tr>
<tr><td>CRM</td><td>13:00</td></tr>
<tr><td>&nbsp;</td><td>14:00</td></tr>
<tr><td>SEP</td><td>14:00</td></tr>
<tr><td>&nbsp;</td><td>16:00</td></tr>
<tr><td>89</td><td></td></tr>
<tr><td>&nbsp;</td><td></td></tr>
</table></div>

<div id="myday_14036"><table class="duties_table">
<tr><td>B001T</td><td></td></tr>
<tr><td>&nbsp;6</td><td></td></tr>
</table></div>

</div></body></html>
"""
        entries = parse(data)
        self.assertEqual(entries, [
            RosterEntry(aims_day='14146',
                        items=('CSBE', '3:00', '5:00', 'B006D')),
            RosterEntry(aims_day='14147', items=('B086',)),
            RosterEntry(aims_day='14150', items=('D/O',)),
            RosterEntry(aims_day='14153', items=('LVE',)),
            RosterEntry(aims_day='14157', items=('==>', 'B253')),
            RosterEntry(aims_day='14162', items=('ADTY', '5:00', '11:00')),
            RosterEntry(aims_day='14174', items=('FTGD',)),
            RosterEntry(aims_day='13869',
                        items = ('FIRE', '8:00', '9:30',
                                 'DOOR', '9:30', '10:45',
                                 'G/S', '10:45', '11:30',
                                 'ASEC', '11:30', '13:00',
                                 'CRM', '13:00', '14:00',
                                 'SEP', '14:00', '16:00',
                                 '89')),
            RosterEntry(aims_day='14036', items=('B001T', '6')),
            ])


    def test_bad_brief_roster(self):
        data = "<html><head></head><body><p>No main div</p></body></html>"
        with self.assertRaises(BadBriefRoster) as cm:
            parse(data)
        data = ("<html><head></head><body><div id='main_div'>"
                "No class=duties_tables tables</div></body></html>")
        with self.assertRaises(BadBriefRoster) as cm:
            parse(data)
        data = "Not even HTML"
        with self.assertRaises(BadBriefRoster) as cm:
            parse(data)
        #no id on parent of duties_table
        data = ("<html><head></head><body><div id='main_div'>"
                "<div><table class=\"duties_table\">"
                "<tr><td>B001T</td><td></td></tr>"
                "<tr><td>&nbsp;6</td><td></td></tr>"
                "</table></div></div></body></html>")
        with self.assertRaises(BadBriefRoster) as cm:
            parse(data)
        #duties_table has no parent
        data = ("<table class=\"duties_table\">"
                "<tr><td>QQQQ</td><td></td></tr>"
                "<tr><td>&nbsp;6</td><td></td></tr>"
                "</table>")
        with self.assertRaises(BadBriefRoster) as cm:
            parse(data)



class TestBriefRosterProcessing(unittest.TestCase):

    def test_roster_processing(self):
        duties_ = duties(
            [
                RosterEntry(aims_day='14146', items=('CSBE', '3:00', '5:00', 'B006D')),
                RosterEntry(aims_day='14147', items=('B086',)),
                RosterEntry(aims_day='14152', items=('D/O',)),
                RosterEntry(aims_day='14153', items=('LVE',)),
                RosterEntry(aims_day='14157', items=('==>', 'B253')),
                RosterEntry(aims_day='14158',
                            items = ('FIRE', '8:00', '9:30',
                                     'DOOR', '9:30', '10:45',
                                     '89')),
            ])
        self.assertEqual(duties_, [
            Duty(start=None, finish=None,
                 trip_id=TripID('14146', 'B006D'),
                 sectors=None),
            Duty(start=datetime.datetime(2018, 9, 24, 3, 0),
                 finish=datetime.datetime(2018, 9, 24, 5, 0),
                 trip_id=TripID('14146', 'CSBE'),
                 sectors=[Sector(
                     name='CSBE',
                     from_=None, to=None,
                     sched_start=datetime.datetime(2018, 9, 24, 3, 0),
                     sched_finish=datetime.datetime(2018, 9, 24, 5, 0),
                     act_start=datetime.datetime(2018, 9, 24, 3, 0),
                     act_finish=datetime.datetime(2018, 9, 24, 5, 0),
                     reg=None, type_=None,
                     flags=SectorFlags.QUASI| SectorFlags.GROUND_DUTY,
                     crewlist_id=None)]),
            Duty(start=None, finish=None,
                 trip_id=TripID('14147', 'B086'),
                 sectors=None),
            Duty(start=None, finish=None,
                 trip_id=TripID('14157', 'B253'),
                 sectors=None),
            Duty(start=None, finish=None,
                 trip_id=TripID('14158', '89'),
                 sectors=None),
            Duty(start=datetime.datetime(2018, 10, 6, 9, 30),
                 finish=datetime.datetime(2018, 10, 6, 10, 45),
                 trip_id=TripID('14158', 'DOOR'),
                 sectors=[Sector(name='DOOR',
                                 from_=None, to=None,
                                 sched_start=datetime.datetime(2018, 10, 6, 9, 30),
                                 sched_finish=datetime.datetime(2018, 10, 6, 10, 45),
                                 act_start=datetime.datetime(2018, 10, 6, 9, 30),
                                 act_finish=datetime.datetime(2018, 10, 6, 10, 45),
                                 reg=None, type_=None,
                                 flags=SectorFlags.QUASI | SectorFlags.GROUND_DUTY,
                                 crewlist_id=None)]),
            Duty(start=datetime.datetime(2018, 10, 6, 8, 0),
                 finish=datetime.datetime(2018, 10, 6, 9, 30),
                 trip_id=TripID('14158', 'FIRE'),
                 sectors=[Sector(name='FIRE', from_=None, to=None,
                                 sched_start=datetime.datetime(2018, 10, 6, 8, 0),
                                 sched_finish=datetime.datetime(2018, 10, 6, 9, 30),
                                 act_start=datetime.datetime(2018, 10, 6, 8, 0),
                                 act_finish=datetime.datetime(2018, 10, 6, 9, 30),
                                 reg=None, type_=None,
                                 flags=SectorFlags.QUASI | SectorFlags.GROUND_DUTY,
                                 crewlist_id=None)]),
        ])


    def test_bad_roster_entries(self):
        #entries not a list or tuple
        with self.assertRaises(AssertionError) as cm:
            duties(RosterEntry(aims_day='14147', items=('B086',)))
        #filter not a list or tuple
        with self.assertRaises(AssertionError) as cm:
            duties(
                [RosterEntry(aims_day='14147', items=('B086',))],
                "filter")
        #wrong type in entries list
        with self.assertRaises(AssertionError) as cm:
            duties(["bad", "list"])
        #aims day empty
        with self.assertRaises(BadRosterEntry) as cm:
            duties([
                RosterEntry(
                    aims_day='',
                    items=('B086',)
                )
            ])
        #aims day not a number
        with self.assertRaises(BadRosterEntry) as cm:
            duties([
                RosterEntry(
                    aims_day='text',
                    items=('B086',)
                )
            ])
        #malformed items -- just one time
        with self.assertRaises(BadRosterEntry) as cm:
            duties([
                RosterEntry(
                    aims_day='14160',
                    items=('8:00',)
                )
            ])
        #malformed items -- two times, no identifier
        with self.assertRaises(BadRosterEntry) as cm:
            duties([
                RosterEntry(
                    aims_day='14160',
                    items=('8:00', '09:00')
                )
            ])
        #malformed item -- bad times
        with self.assertRaises(BadRosterEntry) as cm:
            duties([
                RosterEntry(
                    aims_day='14160',
                    items=('ESBY', '24:00', '25:00')
                )
            ])
