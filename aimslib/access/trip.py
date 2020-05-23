from bs4 import BeautifulSoup #type: ignore
from typing import List
import datetime as DT
import re

from aimslib.access.connect import PostFunc
from aimslib.common.types import (
    TripID, Sector, SectorFlags, Duty,
    BadTripDetails, NoTripDetails, BadAIMSSector, BadAIMSDuty,
)

AimsSector = List[str]
AimsDuty = List[AimsSector]

def retrieve(post: PostFunc, trip_id: TripID) -> str:
    """Downloads and returns the html of a trip sheet.

    :param post: The closure returned from connect.connect()
    :param trip_id: A tuple of the form (aims_day, trip) that uniquely
        identifies the trip. trip is usually a letter or two followed by
        three or four numbers, aims_day is the number of days since 1/1/1980
        in the form of a string.

    :return: The html of an AIMS trip sheet. This is the sheet you get
        if you click a trip identifier on "Crew Schedule - Brief"
        (e.g. B089) then click the "Trip Details in UTC button".
    """
    r = post("perinfo.exe/schedule", {
                 "useGET": "1",
                 "FltInf": "1",
                 "ORGDAY": trip_id.aims_day,
                 "CROUTE": trip_id.trip,
             })
    return r.text


def parse(html:str) -> List[AimsDuty]:
    """Parse trip details out of a AIMS trip sheet.

    :param html: The HTML of an AIMS trip sheet

    :return: Returns a List[AimsDuty]:

    An AimsDuty is a list of AimsSectors. An AimsSector is a list of
    strings found in an AIMS trip sheet. The first six fields always
    exist. They are:

      [0]: Sector identifier (used as input to find crew list)
      [1]: Flight number
      [2]: Departure aerodrome (3 letter code)
      [3]: Arrival aerodrome (3 letter code)
      [4]: Scheduled departure time (HHMM format) in UTC
      [5]: Scheduled arrival time (HHMM format) in UTC

    Field 0 may be None in the case that a standby duty occurred before a
    flight duty, and the standby duty got included on the trip sheet as a
    quasi sector.

    The last field of the last AimsSector is the AimsDuty end time. If
    there is more than one sector, the last field of the first sector is
    the AimsDuty start time. If there is only one sector it is the second
    to last field.

     Other fields of interest occur in the following order, although their
     exact position is not defined:

       [?]: Trip day number (single digit)
       [?]: Actual departure time (Adddd where dddd are digits)
       [?]: Actual arrival time (Adddd where dddd are digits)
       [?]: Tail number. Either XX-XXX or X-XXXX where X are capital
            letters. This may change in the future, although it is likely
            that there will still be a dash either as the 2nd or 3rd
            character.

     Other fields that are not of interest will be in the mix. They mostly
     have the form HH:MM, although the departure date is of the form
     Fri18Jan.
    """
    if html.find("Unable to find the trip details") != -1:
        raise NoTripDetails
    soup = BeautifulSoup(html, "html.parser")
    first_sector = soup.find("tr", class_="mono_rows_ctrl_f3")
    if not first_sector:
        raise BadTripDetails("tr.mono_rows_ctrl_f3 not found")
    id_ = first_sector.get("id", None)
    aims_sector = [id_] + first_sector.text.split()
    aims_duty: AimsDuty = [aims_sector]
    aims_duties = [aims_duty]
    for sibling in first_sector.find_next_siblings("tr"):
        if "mono_rows_ctrl_f3" in sibling["class"]:
            id_ = sibling.get("id", None)
            sector = [id_] + sibling.text.split()
            if len(sector) < 6: #gross error check
                raise BadTripDetails(sibling.text)
            aims_duty.append(sector)
        elif aims_duty != []:
            aims_duty = []
            aims_duties.append(aims_duty)
    if aims_duties[-1] == []: del aims_duties[-1]
    return aims_duties


def _sector(aims_sector: AimsSector, date: DT.date
) -> Sector:
    """Convert an AimsSector object into a Sector object.

    :param aims_sector: An AimsSector object, as described in the
        documentation forparse_trip_details().
    :param date: The date of the sector

    :return: A Sector object.

    Standby and training duties that form part of a trip are recorded
    by AIMS as quasi-sectors. A quasi-sector is identified by its
    flight number being wrapped in square brackets, e.g. [esby]. AIMS
    does not update quasi-sectors with actual times.

    The pax flag indicates a postioning sector. If reg is None, it is
    ground positioning. AIMS does not update ground positioning
    sectors with actual times.

    Accessing AIMS crew member details is relatively slow and the
    planned crew for a sector tends to be in a continuous state of
    flux. Therefore, the crewlist field is only filled for sectors in
    the past; future sectors have an empty list.
    """
    try:
        id_, flightnum, from_, to, sched_off, sched_on = aims_sector[:6]
    except:
        raise BadAIMSSector(str(aims_sector))
    off, on, reg = (None,) * 3
    pax = False
    for field in aims_sector[6:]:
        if re.match(r"A\d{4}", field):
            if not off:
                off = field[1:]
            else:
                on = field[1:]
        elif re.match(r"\w{1,2}-\w{3,5}", field):
            reg = field
        elif field == "PAX":
            pax = True
    try:
        sched_off, sched_on = (X + "+0" if len(X) == 4 else X
                               for X in (sched_off, sched_on))
        sched_off_t, sched_on_t = (DT.datetime.strptime(X[:4], "%H%M").time()
                                   for X in (sched_off, sched_on))
        sched_off_dt = (DT.datetime.combine(date, sched_off_t)
                        + DT.timedelta(days=int(sched_off[5])))
        sched_on_dt = (DT.datetime.combine(date, sched_on_t)
                       + DT.timedelta(days=int(sched_on[5])))
        #actual times don't have +1 for after midnight, so use
        #proximity to schedule
        off_dt, on_dt = None, None
        if on:
            off_t, on_t = (DT.datetime.strptime(X[:4], "%H%M").time()
                           for X in (off, on))
            off_dt, on_dt = (DT.datetime.combine(date, X)
                             for X in (off_t, on_t))
            if sched_off_dt - off_dt > DT.timedelta(days=1) / 2:
                off_dt += DT.timedelta(days=1)
            if sched_on_dt - on_dt > DT.timedelta(days=1) / 2:
                on_dt += DT.timedelta(days=1)
    except:
        raise BadAIMSSector(str(date) + ", " + str(aims_sector))
    flags = SectorFlags.POSITIONING if pax else SectorFlags.NONE
    if not id_: flags |= SectorFlags.QUASI
    if not reg: flags |= SectorFlags.GROUND_DUTY
    return Sector(flightnum, from_, to,
                  sched_off_dt, sched_on_dt, off_dt, on_dt,
                  reg, None, flags, id_)



def _duty(aims_duty: AimsDuty, trip_id: TripID, trip_day: int) -> Duty:
    """Create a Duty object from an AimsDuty object.

    :param aims_duty: An AimsDuty object to convert
    :param start_date: The start date of the duty.
    :param trip_id: The id of the trip that the duty belongs to.

    :return: A Duty object.
    """
    start_date = (
        DT.datetime(1980, 1, 1) +
        DT.timedelta(int(trip_id.aims_day))
    ).date()
    try:
        #trip_day = int(aims_duty[0][7]) - 1
        #bug in AIMS makes every trip_day 1, so assume multiple duties
        #occur on incremental days
        date = start_date + DT.timedelta(days=trip_day)
        #fix for AIMS bug where end of duty can have non-existent time 24:00
        if aims_duty[-1][-1] == "24:00": aims_duty[-1][-1] = "00:00"
        duty_end_time = DT.datetime.strptime(
            aims_duty[-1][-1], "%H:%M").time()
        index = -2 if len(aims_duty) == 1 else -1
        duty_start_time = DT.datetime.strptime(
            aims_duty[0][index], "%H:%M").time()
    except:
        raise BadAIMSDuty(str(aims_duty))
    duty_start, duty_end = (
        DT.datetime.combine(date, X)
        for X in (duty_start_time, duty_end_time))
    if duty_end < duty_start:
        duty_end += DT.timedelta(days=1)
    sectors = [] # type: List[Sector]
    for aims_sector in aims_duty:
        sectors.append(_sector(aims_sector, date))
    return Duty(trip_id, duty_start, duty_end, sectors)


def duties(aims_duties: List[AimsDuty], trip_id: TripID) -> List[Duty]:
    """Process a list of AimsDuty objects into a list of Duty objects.

    :param aims_duties: A list of AimsDuty objects, as output by parse
    :param trip_id: The TripID object associated with this trip
    """
    duty_list: List[Duty] = []
    for c, aims_duty in enumerate(aims_duties):
        duty_list.append(_duty(aims_duty, trip_id, c))
    return duty_list
