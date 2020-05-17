# aimslib #

This is a refactor from various different projects to move the functionality of
extracting information from AIMS servers into a common library. It is built and
tested against easyJet AIMS servers. It will likely need adapting to work with
AIMS servers run by other airlines.

## Example code ###
```python
import json
import sys

from aimslib.access.connect import connect, logout
from  aimslib.access.cache import TripCache, CrewlistCache
from aimslib.common.types import NoTripDetails
import aimslib.access.brief_roster as Roster

#put your own values in here
CACHE_DIR = "/SUITABLE/LOCATION/FOR/CACHE/"
ECREW_LOGIN_PAGE = "https://ECREW/LOGIN/PAGE"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"


def heartbeat():
    sys.stderr.write('.')
    sys.stderr.flush()

#connect to AIMS
post_func = connect(ECREW_LOGIN_PAGE, USERNAME, PASSWORD, heartbeat)

#build a sparse duty list from the current brief roster and the two before
sparse_dutylist = []
for roster in Roster.retrieve(post_func, -2):
    sparse_dutylist.extend(Roster.duties(Roster.parse(roster)))

#build an expanded duty list using trip pages
expanded_dutylist = []
trip_cache = TripCache(CACHE_DIR + "aimslib.tripcache", post_func)
last_id = None
for duty in sorted(sparse_dutylist):
    if duty.trip_id == last_id: continue #sparse_dutylist may contain duplicates
    last_id = duty.trip_id
    if duty.start is None:
        try:
            expanded_dutylist.extend(trip_cache.trip(duty.trip_id))
        except NoTripDetails:
            print("Trip details not found for: ", duty.trip_id, file=sys.stderr)
    else:
        expanded_dutylist.append(duty)
trip_cache.store()

#build crewlist map
crew_cache = CrewlistCache(CACHE_DIR + "aimslib.clcache", post_func)
crewlist_map = {}
for duty in expanded_dutylist:
    if duty.sectors:
        for sector in duty.sectors:
            if not sector.crewlist_id: continue
            crewlist = crew_cache.crewlist(sector.crewlist_id)
            crewlist_map[sector.crewlist_id] = crewlist
crew_cache.store()

#dump objects as json
print(json.dumps(
    (expanded_dutylist, crewlist_map),
    default=lambda o: str(o),
    indent=2))

#cleanup
logout(post_func)

```
