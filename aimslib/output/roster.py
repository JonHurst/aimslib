#!/usr/bin/python3

from typing import List
from dateutil import tz

from aimslib.common.types import Duty, SectorFlags


def roster(duties: List[Duty]) -> str:
    output = []
    for duty in duties:
        if not duty.sectors: continue
        start, end = [X.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
                      for X in (duty.start, duty.finish)]
        duration = int((end - start).total_seconds()) // 60
        from_ = None
        airports = []
        block = 0
        for sector in duty.sectors:
            if not from_ and sector.from_: from_ = sector.from_
            if sector.flags & SectorFlags.QUASI:
                airports.append(sector.name)
            elif sector.flags & SectorFlags.POSITIONING:
                airports.append("[psn]")
            else:
                off, on = sector.sched_start, sector.sched_finish
                block += int((on - off).total_seconds()) // 60
            if sector.to: airports.append(sector.to)
        if from_: airports = [from_] + airports
        duration_str = f"{duration // 60}:{duration % 60:02d}"
        block_str = f"{block // 60}:{block % 60:02d}"
        output.append(f"{start:%d/%m/%Y %H:%M}-{end:%H:%M} "
                      f"{'-'.join(airports)} {block_str}/{duration_str}")
    return "\n".join(output)
