import csv as libcsv
import io
from typing import List, Dict

from aimslib.common.types import Duty, CrewMember, SectorFlags


def csv(duties: List[Duty], crews: Dict[str, List[CrewMember]], fo:bool
) -> str:
    output = io.StringIO(newline='')
    fieldnames = ['Off Blocks', 'On Blocks', 'Origin', 'Destination',
                  'Registration', 'Type', 'Captain', 'Role', 'Crew']
    fieldname_map = (('Off Blocks', 'act_start'), ('On Blocks', 'act_finish'),
                     ('Origin', 'from_'), ('Destination', 'to'),
                     ('Registration', 'reg'), ('Type', 'type_'))
    writer = libcsv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction='ignore',
        dialect='unix')
    writer.writeheader()
    for duty in duties:
        if not duty.sectors: continue
        for sector in duty.sectors:
            if (sector.flags != SectorFlags.NONE or
                not (sector.act_start and sector.act_finish)): continue
            sec_dict = sector._asdict()
            for fn, sfn in fieldname_map:
                sec_dict[fn] = sec_dict[sfn]
            sec_dict['Role'] = 'p1s' if fo else 'p1'
            crewlist = crews.get(sector.crewlist_id, [])
            sec_dict['Captain'] = 'Self'
            if fo and crewlist and crewlist[0].role == 'CP':
                sec_dict['Captain'] = crewlist[0].name
            crewstr = "; ".join([f"{X[1]}:{X[0]}" for X in crewlist])
            if (not sector.type_ and len(sector.crewlist_id) > 3
                and sector.crewlist_id[-3:] in ("319", "320", "321")):
                sec_dict['Type'] = f"{sector.crewlist_id[-3:]}"
            sec_dict['Crew'] = crewstr
            writer.writerow(sec_dict)
    output.seek(0)
    return output.read()
