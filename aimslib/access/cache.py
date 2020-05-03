import pickle
from typing import List, Dict
import os
import datetime as DT

from aimslib.access.connect import PostFunc
from aimslib.common.types import TripID, Duty, CrewMember, SectorFlags
import aimslib.access.trip as Trip
import aimslib.access.crew as Crew

class Cache:

    def __init__(self, filename:str, post: PostFunc):
        self.pickle_file = filename
        self.post_func = post
        try:
            os.mkdir(os.path.dirname(filename))
        except FileExistsError:
            pass
        try:
            with open(filename, "rb") as f:
                self.cache = pickle.load(f)
        except OSError:
            pass #empty cache will be used


    def store(self):
        with open(self.pickle_file, "wb") as f:
            pickle.dump(self.cache, f)


class TripCache(Cache):

    def __init__(self, filename:str, post:PostFunc):
        self.cache: Dict[str, List[Duty]] = {}
        Cache.__init__(self, filename,  post)


    def trip(self, trip_id: TripID) -> List[Duty]:
        if trip_id not in self.cache or self.needs_refresh_p(trip_id):
            self.cache[trip_id] = (
                Trip.duties(
                    Trip.parse(
                        Trip.retrieve(self.post_func, trip_id)), trip_id))
        return self.cache[trip_id]


    def needs_refresh_p(self, trip_id: TripID) -> bool:
        all_actuals_recorded = True
        duty_list = self.cache[trip_id]
        day_later = DT.datetime.utcnow() + DT.timedelta(days=1)
        if duty_list[0].start > day_later:
            return False #cached version is more than one day in the future
        for duty in duty_list:
            if not all_actuals_recorded: break
            for sector in duty.sectors:
                #Ground duties _never_ get updated so no point refreshing
                if sector.flags & SectorFlags.GROUND_DUTY: continue
                if sector.act_start is None or sector.act_finish is None:
                    all_actuals_recorded = False
                    break
        if all_actuals_recorded:
            return False #cached version finalised
        return True



class CrewlistCache(Cache):

    def __init__(self, filename:str, post: PostFunc):
        self.cache: Dict[str, List[CrewMember]] = {}
        Cache.__init__(self, filename, post)


    def crewlist(self, crewlistID: str) -> List[CrewMember]:
        if crewlistID in self.cache:
            return self.cache[crewlistID]
        crewlist = Crew.crewlist(Crew.retrieve(self.post_func, crewlistID))
        #first part of identifier is an AIMS data (days since 1980-01-01)
        aims_date = crewlistID.split(",", 1)[0]
        date = DT.date(1980, 1, 1) + DT.timedelta(days=int(aims_date))
        #only cache crewlists from more than 2 days ago
        if DT.date.today() - date > DT.timedelta(days=2):
            self.cache[crewlistID] = crewlist
        return crewlist
