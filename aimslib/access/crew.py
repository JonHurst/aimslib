from bs4 import BeautifulSoup
from aimslib.common.types import BadCrewList, CrewMember
from typing import List

from aimslib.access.connect import PostFunc

def retrieve(post: PostFunc, id_: str) -> str:
    """Downloads and returns the html of a crewlist.

    :param post: Closure returned from connect.connect()
    :param id_: The crew identifier. It looks something like:

            '14262,138549409849,14262,401,brs,1, ,gla,320'

    :return: The HTML of a crew sheet. This is the page you get when you
        click a sector on an AIMS duty sheet.
    """
    r = post("perinfo.exe/getlegmem",{"useGet": "1", "LegInfo": id_})
    return r.text


def crewlist(html: str) -> List[CrewMember]:
    """Convert an AIMS HTML crew list into a crew list.

    :param html: The HTML of the AIMS crew list.

    :return: A list of CrewMember objects. A CrewMember object is a named
        tuple consisting of a name and a role.
    """
    html = html.replace("\n</tr><tr class=", "\n<tr class=") #fix buggy html
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find("tr", class_="sub_table_header")
    if not header:
        raise BadCrewList
    crewlist = []
    for sibling in header.find_next_siblings("tr"):
        crew_strings = [X.text for X in sibling.find_all("td")]
        if crew_strings[8] == "*": continue #ignore positioning crew
        crewlist.append(CrewMember(crew_strings[1].title(), crew_strings[5]))
    return crewlist
