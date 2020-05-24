from typing import List, Dict
import os.path
import sys

from  aimslib.access.cache import TripCache, CrewlistCache
from aimslib.common.types import Duty, NoTripDetails, CrewMember
import aimslib.access.brief_roster as Roster


CACHE_DIR = os.path.expanduser("~/.cache/")


def duties(post_func, months: int) -> List[Duty]:
    sparse_dutylist = []
    if months < 0: months += 1
    else: months -= 1
    for r in Roster.retrieve(post_func, months):
        sparse_dutylist.extend(Roster.duties(Roster.parse(r)))
    expanded_dutylist = []
    trip_cache = TripCache(CACHE_DIR + "aimslib.tripcache", post_func)
    last_id = None
    for duty in sorted(sparse_dutylist):
        if duty.trip_id == last_id: continue #avoid duplicates
        last_id = duty.trip_id
        if duty.start is None:
            try:
                expanded_dutylist.extend(trip_cache.trip(duty.trip_id))
            except NoTripDetails:
                print(f"Trip details not found for: {duty.trip_id}",
                      file=sys.stderr)
        else:
            expanded_dutylist.append(duty)
    trip_cache.store()
    return expanded_dutylist


def crew(post_func, dutylist: List[Duty]) -> Dict[str, List[CrewMember]]:
    crew_cache = CrewlistCache(CACHE_DIR + "aimslib.clcache", post_func)
    crewlist_map = {}
    for duty in dutylist:
        if duty.sectors:
            for sector in duty.sectors:
                if not sector.crewlist_id: continue
                crewlist = crew_cache.crewlist(sector.crewlist_id)
                crewlist_map[sector.crewlist_id] = crewlist
    crew_cache.store()
    return crewlist_map
