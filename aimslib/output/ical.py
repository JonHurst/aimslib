from typing import Dict, List
import datetime as dt

from aimslib.common.types import Duty, SectorFlags

vcalendar = """\
BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:hursts.org.uk\r
{}\r
END:VCALENDAR\r
"""

vevent = """\
BEGIN:VEVENT\r
UID:{uid}\r
DTSTAMP:{modified}\r
DTSTART:{start}\r
DTEND:{end}\r
SUMMARY:{route}\r
{sectors}\
LAST-MODIFIED:{modified}\r
SEQUENCE:0\r
STATUS:TENTATIVE\r
END:VEVENT"""

ical_datetime = "{:%Y%m%dT%H%M%SZ}"


def _build_dict(duty: Duty) -> Dict[str, str]:
    event = {}
    event["start"] = ical_datetime.format(duty.start)
    event["end"] = ical_datetime.format(duty.finish)
    sector_strings = []
    airports = []
    from_ = None
    for sector in duty.sectors:
        if not from_ and sector.from_: from_ = sector.from_
        if sector.flags & SectorFlags.QUASI:
            airports.append(sector.name)
        elif sector.flags & SectorFlags.POSITIONING:
            airports.append("[psn]")
        if sector.to: airports.append(sector.to)
        off, on = sector.sched_start, sector.sched_finish
        from_to = ""
        if sector.from_ and sector.to:
            from_to = f"{sector.from_}/{sector.to} "
        sector_strings.append(
            f"{off:%H:%M}z-{on:%H:%M}z {sector.name} "
            f"{from_to}"
            f"{sector.reg if sector.reg else ''}")
    if from_: airports = [from_] + airports
    event["sectors"] = "DESCRIPTION:{}\r\n".format(
        "\\n\r\n ".join(sector_strings))
    event["uid"] = "{}{}@HURSTS.ORG.UK".format(
        duty.start.isoformat(), "".join(airports))
    event["route"] = "-".join(airports)
    event["modified"] = ical_datetime.format(dt.datetime.utcnow())
    return event

def ical(duties: List[Duty]) -> str:
    events = []
    for duty in duties:
        d = _build_dict(duty)
        events.append(vevent.format(**d))
    return vcalendar.format("\r\n".join(events))
