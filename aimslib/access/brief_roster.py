from bs4 import BeautifulSoup #type: ignore
from typing import List, NamedTuple
import datetime as DT

from aimslib.access.connect import PostFunc
from aimslib.common.types import Duty, TripID, BadBriefRoster


class RosterEntry(NamedTuple):
    aims_day: str
    items: List[str]


def retrieve(post: PostFunc, offset: int = 0) -> str:
    """Downloads the html of a brief roster.

    :param post: Function to call for sending requests to AIMS
    :offset: The offset from the 'current' brief roster

    :return: html string containing the requested brief roster

    Unfortunately, as far as I can tell the "brief roster"
    functionality of AIMS can only move from one roster to either the
    next or previous roster. This means if the absolute value of the
    offset is greater than 1, all intermediary rosters have to be
    downloaded. This makes the process of stepping to a distant roster
    very slow.
    """
    r = post("perinfo.exe/schedule", {})
    if offset:
        direc = "2" if offset > 0 else "1"
        for _ in range(abs(offset)):
            r = post("perinfo.exe/schedule", {"Direc": direc,  "_flagy": "2"})
    return r.text


def parse(html: str) -> List[RosterEntry]:
    """Convert an HTML brief roster to a list of roster entries.

    :param html: The HTML of an AIMS Brief Roster

    :return: A list of RosterEntry objects. A RosterEntry object is a tuple
        consisting of an aims_day and a list of strings. An aims_day is an
        integer representing the number of elapsed days since 1st January
        1980 that is used internally by AIMS. The list of strings is the
        strings that AIMS allocated to that day of the brief roster in
        reading order.

    There appear to be four categories of strings published on an
    AIMS brief roster:

    1. Strings indicating some form of day off. These include D/O,
    D/OR, WD/O, LVE, P/T, REST, FTGD and SICK. There may be others.

    2. Strings indicating some form of standby ot training duty. These
    can be identified as a group of three strings, the latter two of
    which are times in the form h:mm or hh:mm.

    3. A single digit number. These seem to be associated with long
    duties that have additional rest limitations associated with them.

    4. Trip identifiers and continuation markers. A trip identifier is
    a string consisting of a mix of letters and numbers. They seem to
    generally be a letter or two, some numbers and maybe another
    letter, but I have come across trip identifiers that are just two
    digit numbers. It is easiest to identify them as strings that do
    not belong to any of the other groups, although not having a
    guaranteed complete set of category 1 strings complicates
    this. Continuation markers are "==>", indicating that the previous
    day's trip crosses midnight.

    """
    soup = BeautifulSoup(html, "html.parser")
    main_div = soup.find("div", id="main_div")
    if not main_div: raise BadBriefRoster
    duties_tables = main_div.find_all("table", class_="duties_table")
    if not duties_tables: raise BadBriefRoster
    roster_entries: List[RosterEntry] = []
    for table in duties_tables:
        roster_entries.append(RosterEntry(
            table.parent["id"].replace("myday_", ""),
            [X for X in table.stripped_strings]))
    return roster_entries


def duties(entries: List[RosterEntry]) -> List[Duty]:
    """Convert a list of RosterEntry objects into a list of Duty objects.

    :param entries: a list of RosterEntry objects

    :return: A list of Duty objects. There may be multiple Duty objects
        associated with each RosterEntry. Duty objects for trips only have
        the trip identifier, since that is all that is available from the
        brief roster page.
    """
    duty_list: List[Duty] = []
    for entry in entries:
        while len(entry.items):
            p = entry.items.pop()
            if p in ("==>", "D/O", "D/OR", "WD/O", "P/T", "LVE", "FTGD",
                     "REST", "SICK", "SIDO", "SILN"): continue
            elif len(p) >= 4 and p[-3] == ":": #found a time
                end_time = DT.datetime.strptime(p, "%H:%M").time()
                p = entry.items.pop()
                start_time = DT.datetime.strptime(p, "%H:%M").time()
                text = entry.items.pop()
                date = (DT.datetime(1980, 1, 1) +
                        DT.timedelta(int(entry.aims_day))).date()
                start, end = [DT.datetime.combine(date, X)
                              for X in (start_time, end_time)]
                if end < start:
                    end += DT.timedelta(days=1)
                duty_list.append(
                    Duty(start, end, TripID(entry.aims_day, text), None))
            else: #should be a trip identifier
                duty_list.append(
                    Duty(None, None, TripID(entry.aims_day, p), None))
    return duty_list
