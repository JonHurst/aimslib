import requests
from bs4 import BeautifulSoup #type: ignore
from typing import List

from aimslib.access.connect import REQUEST_TIMEOUT
from aimslib.common.types import BadTripDetails, NoTripDetails


AimsSector = List[str]
AimsDuty = List[AimsSector]


def get_trip(
        session: requests.Session,
        base_url: str,
        aims_day: str,
        trip: str
) -> str:
    """Downloads and returns the html of a trip sheet.

    :param aims_day: The number of days since 1/1/1980 as a string.
    :param trip: The identifier that AIMS uses to define a trip. Usually a
        letter or two followed by three or four numbers.

    :return: The html of an AIMS trip sheet. This is the sheet you get
        if you click a trip identifier on "Crew Schedule - Brief"
        (e.g. B089) then click the "Trip Details in UTC button".
    """
    r = session.get(base_url + "perinfo.exe/schedule",
                    params={
                        "FltInf": "1",
                        "ORGDAY": aims_day,
                        "CROUTE": trip,
                    },
                    timeout=REQUEST_TIMEOUT)
    return r.text


def parse_trip_details(html:str) -> List[AimsDuty]:
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
