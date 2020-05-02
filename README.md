# aimslib #

This is a refactor from various different projects to move the functionality of
extracting information from AIMS into a common library.

## Example code ###
```python
import json
import sys

from aimslib.access.connect import connect, logout
from  aimslib.access.cache import TripCache, CrewlistCache
import aimslib.access.brief_roster as Roster

def heartbeat():
    sys.stderr.write('.')
    sys.stderr.flush()

#connect to server
post_func = connect(
    "https://PATH.TO.LOGIN.PAGE",
    "USERNAME",
    "PASSWORD",
    heartbeat)

#build expanded duty list
trip_cache = TripCache("/SUITABLE/PATH/FOR/CACHEFILE/aimslib.tripcache", post_func)
roster = Roster.duties(Roster.parse(Roster.retrieve(post_func, -2)))
expanded_dutylist = []
for duty in roster:
    if duty.start is None:
        expanded_dutylist.extend(trip_cache.trip(duty.trip_id))
    else:
        expanded_dutylist.append(duty)
trip_cache.store()

#build crewlist map
crew_cache = CrewlistCache("/SUITABLE/PATH/FOR/CACHEFILE/aimslib.clcache", post_func)
crewlist_map = {}
for duty in expanded_dutylist:
    if duty.sectors:
        for sector in duty.sectors:
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
