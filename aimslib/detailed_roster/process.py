#!/usr/bin/python3
#coding=utf-8

# Copyright 2011 Jon Hurst
# This file is part of aimslib.

#     aimslib is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     aimslib is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with process-roster.  If not, see <http://www.gnu.org/licenses/>.

import re
import datetime
from html.parser import HTMLParser
from typing import List, Dict, Tuple

import aimslib.common.types as T


class InputFileException(Exception):
    def __str__(self):
        return "Input file does not appear to be an AIMS detailed roster"


class RosterParser(HTMLParser):

    def __init__(self):
        self.output_list = [[]]
        self.in_td = False
        HTMLParser.__init__(self)


    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.in_td = True
            self.output_list[-1].append("")
        elif tag == "br":
            if self.in_td:
                self.output_list[-1][-1] += "\n"


    def handle_endtag(self, tag):
        if tag == "td":
            self.in_td = False
        elif tag == "tr":
            self.output_list.append([])
        pass


    def handle_data(self, data):
        if self.in_td:
            self.output_list[-1][-1] += data


def lines(roster):
    """
    Turn an AIMS roster into a list of lines, each line being represented by a list of cells.

    The input should be a string containing the HTML file of an AIMS detailed roster.
    The output has the form:

    [
        [ line0cell0, line0cell1, ..., line0cell31],
        [ line1cell0, line1cell1, ..., line1cell31],
        ...
        [ lineNcell0, lineNcell1, ..., lineNcell31]
    ]

    """
    parser = RosterParser()
    parser.feed(roster)
    if (len(parser.output_list) < 10 or
        len(parser.output_list[1]) < 1 or
        not parser.output_list[1][0].startswith("Personal")):
        raise InputFileException
    return parser.output_list


def extract_date(lines):
    """
    Return the date as found in the Period: xx/xx/xxxx clause of an AIMS detailed roster

    The input is 'lines' format as detailed in the lines() docstring.
    The output is a datetime.date object with the first day that the roster is applicable.
    """
    mo = re.search(r"Period: (\d{2}/\d{2}/\d{4})", lines[1][0])
    return datetime.datetime.strptime(mo.group(1), "%d/%m/%Y").date()


def columns(lines):
    """
    Convert 'lines' format input to 'columns' format output.

    The input is 'lines' format as detailed in the lines() docstring.
    The output is a list of columns built from the rows with 32 cells that occur before
    the word Block is found in the row. It has the form:

    [
        [Col0Cell0, Col0Cell1, ...],
        [Col1Cell0, Col1Cell1, ...],
        ...
        [ColNCell0, ColNCell1, ...]
    ]
    """
    #assumption: main table starts on row 5 of the page 1 table
    width = len(lines[5])
    columns = [[] for _ in range(width)]
    for l in lines[5:]:
        if len(l) != width: continue
        if "Block" in l: break #The last line contains the word "Block"
        for c, e in enumerate(l):
            columns[c].append(e.strip())
    return columns


class Break:
    """
    Gaps between duties.

    A Break of type LINE indicates a gap between duties in a roster column.
    A Break of type COLUMN indicates the gap between the end of one column and
    the start of the next.
    A Break of type DUTY indicates a gap where rest is taken.

    As the data formats move from the fairly raw 'Columns' format to the final
    'Duty List' format, Breaks are replaced by data structure.
    """

    LINE, COLUMN, DUTY = range(0, 3)

    def __init__(self, break_type):
        self.type = break_type


    def __str__(self):
        return ("Line break", "Column break", "Duty break")[self.type]


class Event:
    """A string plus a date stamp.

    The text attribute references a flight number of a sector flown, an airfield departed from or
    arrived at, or a standbylike duty undertaken. The date attribute marks the date that these
    Events occured on.
    """

    def __init__(self, date, text):
        self.date = date
        self.text = text


    def __repr__(self):
        return str(self.date) + ": " + self.text


def event_stream(date, columns):
    """Concatenates columns into a stream of datetime, Event and Break objects

    Input is the date of the first column and a 'columns' data structure as described in the
    columns() function's docstring.
    Output is a list obtained by concatenating the columns and translating all relevant cells
    into datetime, Event or Break objects.
    """
    eventstream = [Break(Break.COLUMN)]
    for c in columns:
        if c[0] == "": break #column has no header means we're finished
        for entry in c[1:]:
            if entry == "" and not isinstance(eventstream[-1], Break):
                eventstream.append(Break(Break.LINE))
            elif (len(entry) <= 2 or #ignore single and double letter codes, e.g. r, M, NM
                  entry[0] == "(" or #ignore any bracketed code
                  entry == "EZS"): #ignore code indicating an EZS flight
                pass
            elif len(entry) == 5 and entry[2] == ":": #found a time
                if entry == "24:00":#bug workaround: roster uses non-existent time "24:00"
                    eventstream.append(datetime.datetime.combine(date + datetime.timedelta(days=1),
                                                                datetime.time(0,0)))
                else:
                    time = datetime.time(int(entry[:2]), int(entry[3:]))
                    eventstream.append(datetime.datetime.combine(date, time))
            else:
                eventstream.append(Event(date, entry))
        date += datetime.timedelta(days=1)
        #remove trailing line break
        if isinstance(eventstream[-1], Break): del eventstream[-1]
        #append the column break
        eventstream.append(Break(Break.COLUMN))
    #there is a corner case where a sector finish time is dragged into the next column
    #by a duty time finishing after midnight, and another where a sector time uses 24:00
    #as a start time but advances this to where 00:00 should correctly sit. To counteract
    #these cases, make sure datetimes in a reversed eventstream only ever decrease.
    eventstream.reverse()
    for c, e in enumerate(eventstream):
        if isinstance(e, Break) and e.type == Break.COLUMN:
            last_datetime = datetime.datetime(9999, 1, 1)
        elif isinstance(e, datetime.datetime):
            if e > last_datetime:
                e -= datetime.timedelta(days=1)
                eventstream[c] = e
            last_datetime = e
    eventstream.reverse()
    return eventstream


def duty_stream(eventstream):
    """Processed an eventstream into a list of sublists, each sublist being the event stream of a duty
    block.

    The input is an 'Event stream' as described in the event_stream() function's docstring. The
    function removes or replaces column breaks with line breaks as appropriate, then splits the
    stream into substreams where 8 hours or more of rest appear to be available.

    Output is of the form:

    [
        [/duty block event stream 1/], [/duty block event stream 2/], ...]
    ]
    """
    #process column breaks, either to line breaks or by removal
    c = 2
    while c < len(eventstream) - 2:
        if isinstance(eventstream[c], Break) and eventstream[c].type == Break.COLUMN:
            #if the column break is preceded by a time but not followed by a time, or
            #if there is a break two entries prior, it is a line break
            if ((isinstance(eventstream[c-1], datetime.datetime) and
                 not isinstance(eventstream[c+1], datetime.datetime)) or
                isinstance(eventstream[c-2], Break)):
                eventstream[c] = Break(Break.LINE)
                c += 1
            else:
                del eventstream[c]
        else:
            c += 1
    #change line breaks to duty breaks around all day duties
    c = 2
    while c < len(eventstream):
        #should only be line breaks in the field at this point
        if isinstance(eventstream[c], Break) and isinstance(eventstream[c-2], Break):
            #if there is a break two entries prior, both are duty breaks
            eventstream[c] = eventstream[c-2] = Break(Break.DUTY)
        c += 1
    #change line breaks to duty breaks where the difference between times is greater than 8 hours
    c = 2
    while c < len(eventstream) - 2:
        if (isinstance(eventstream[c], Break) and
            eventstream[c].type == Break.LINE and
            eventstream[c+2] - eventstream[c-1] > datetime.timedelta(hours=8)):
            eventstream[c] = Break(Break.DUTY)
        c += 1
    #split up eventstream at duty breaks
    duties = [[]]
    for e in eventstream[1:-1]:
        if isinstance(e, Break) and e.type == Break.DUTY:
            duties.append([])
        else:
            duties[-1].append(e)
    return duties


def duty_list(duties):
    """Converts a 'Duty stream' into a 'Duty list'

    The input is a duty stream as detailed in the duty_stream function's docstring. Final fixups are
    made and data in the following 'Duty list' format is returned:

    [
    [TripID, [DutyStart, DutyEnd], [/duty/],...],
    ...
    ]

    where [/duty/] can be:

    1. A Sector of form [Flight#, OffBlocks, From, To, OnBlocks]
    2. A Standbylike of form [Type, Start, End]
    3. An all day duty of the form [Type]. In this case DutyStart and DutyEnd are set to None
    """
    retval = []
    #the end of the last duty may not be included on the roster if it finishes after midnight. For
    #consistency, fake the end of this duty if necessary
    if (len(duties[-1]) >= 2 and
        isinstance(duties[-1][-1], Event) and
        isinstance(duties[-1][-2], datetime.datetime)):
        faketime = datetime.datetime.combine(duties[-1][-2].date() + datetime.timedelta(days=1), datetime.time.min)
        duties[-1] += [Event(faketime.date(), "???"), faketime, faketime]
    #create a retval entry from each duty
    for d in duties:
        aims_day = str((d[0].date - datetime.date(1980, 1, 1)).days)
        retval_entry = [T.TripID(aims_day, d[0].text)]
        #if there is only one item in the duty, it must be an all day duty
        if len(d) == 1:
            retval_entry += [[None, None], [d[0].text]]
        else:
            #otherwise split into sectors at line breaks
            sectors = [[]]
            for entry in d:
                if isinstance(entry, Break):
                    sectors.append([])
                elif isinstance(entry, Event):
                    sectors[-1].append(entry.text)
                else:
                    sectors[-1].append(entry)
            #duty times can be extracted from first and last sectors
            retval_entry += [[sectors[0][1], sectors[-1][-1]]]
            #We may or may not need to remove the "start duty" entry from anything other than last entry
            for s in sectors[:-1]:
                if len([X for X in s if isinstance(X, datetime.datetime)]) >= 3: del s[1]
            #The last entry may need the finish duty time stripping.
            if len([X for X in sectors[-1] if isinstance(X, datetime.datetime)]) == 3: del sectors[-1][-1]
            #Single sector case
            if (len(sectors) == 1 and
                len([X for X in sectors[0] if isinstance(X, datetime.datetime)]) == 4):
                del sectors[0][1]
                del sectors[0][-1]
            #add sectors to retval entry
            retval_entry += sectors
        retval.append(retval_entry)
    return retval


def _clean_name(name: str) -> str:
    return " ".join([X.strip().capitalize() for X in name.split()])


def crew(roster: str, duties: List[T.Duty]=[]
) -> Dict[str, Tuple[T.CrewMember, ...]]:
    """Extract the crew lists from the text of an AIMS detailed roster.
    """
    #create a mapping of the form {allkey: [crewlist_id1, ...], } to allow
    #crew with flights listed as all to be assigned to sector ids.
    sector_map: Dict[str, List[str]] = {}
    for duty in duties:
        if not duty.sectors: continue
        key_all = f"{duty.start:%Y%m%d}All~"
        sector_map[key_all] = []
        for sector in duty.sectors:
            if not sector.crewlist_id: continue
            sector_map[key_all].append(sector.crewlist_id)
    retval = {}
    crew_string = ""
    ls = lines(roster)
    for c, l in enumerate(ls):
        if len(l) == 0: continue
        mo = re.match(r"DATE\s*RTES\s*NAMES", l[0])
        if mo:
            if c + 1 < len(ls):
                crew_string = ls[c + 1][0].replace(" ", " ")
            break
    if crew_string != "":
        s = re.split("(\d{2}/\d{2}/\d{4})", crew_string)
        s = [X.strip() for X in s]
        dates = s[1::2]
        #entries is a list of lists of the form [[route, role, name, role, name, ...], ...]
        entries = [re.split(r"\s*(\w{2})> ", X) for X in s[2::2]]
        for (d, e) in zip(dates, entries):
            for flight in e[0].split(","):
                key = f"{d[6:10]}{d[3:5]}{d[0:2]}{flight}~"
                crew = zip(e[2::2], e[1::2])
                retval[key] = tuple(
                    [T.CrewMember(_clean_name(X[0]), X[1]) for X in crew])
                #add keys for individual sectors where flight is listed as all
                if key in sector_map:
                    for id_ in sector_map[key]:
                        retval[id_] = retval[key]
    return retval


def duties(s: str) -> List[T.Duty]:
    l = lines(s)
    c = columns(l)
    es = event_stream(extract_date(l), c)
    ds = duty_stream(es)
    dl = duty_list(ds)
    ret: List[T.Duty] = []
    for duty in dl:
        if duty[1][1] is None: continue
        sectors: List[T.Sector] = []
        for sector in duty[2:]:
            if len(sector) == 3:
                sectors.append(T.Sector(
                    name=sector[0],
                    from_=None, to=None,
                    sched_start=sector[1], sched_finish=sector[2],
                    act_start=sector[1], act_finish=sector[2],
                    reg=None, type_=None, crewlist_id=None,
                    flags=T.SectorFlags.QUASI | T.SectorFlags.GROUND_DUTY))
            else:
                from_ = sector[2]
                flags = T.SectorFlags.NONE
                if from_[0] == "*":
                    from_ = from_[1:]
                    flags = T.SectorFlags.POSITIONING
                if sector[0] == "TAXI":
                    flags |= T.SectorFlags.GROUND_DUTY
                sectors.append(T.Sector(
                    name=sector[0],
                    from_=from_, to=sector[3],
                    sched_start=sector[1], sched_finish=sector[4],
                    act_start=sector[1], act_finish=sector[4],
                    reg=None, type_=None,
                    crewlist_id=f"{sector[1]:%Y%m%d}{sector[0]}~",
                    flags=flags))
        ret.append(T.Duty(duty[0], duty[1][0], duty[1][1], sectors))
    return ret
