import typing as T
import datetime as DT
import enum


class CrewMember(T.NamedTuple):
    name: str
    role: str


class SectorFlags(enum.Enum):
    POSITIONING = enum.auto()
    GROUND_DUTY = enum.auto()


class Sector(T.NamedTuple):
    name: str
    from_: T.Optional[str]
    to: T.Optional[str]
    sched_start: DT.datetime
    sched_finish: DT.datetime
    act_start: DT.datetime
    act_finish: DT.datetime
    reg: T.Optional[str]
    flags: SectorFlags
    crewlist_id: str


class TripID(T.NamedTuple):
    aims_day: str
    trip: str


class Duty(T.NamedTuple):
    start: T.Optional[DT.datetime]
    finish: T.Optional[DT.datetime]
    trip_id: TripID
    sectors: T.Optional[T.List[Sector]]


class AIMSException(Exception):
    def __init__(self, str_: str ="") -> None:
        self.str_ = str_


class LogonError(AIMSException):
    """Logon failed."""
    pass


class UsernamePasswordError(AIMSException):
    """Username or password incorrect."""
    pass


class BadBriefRoster(AIMSException):
    """Brief Roster parse failed."""
    pass

class BadTripDetails(AIMSException):
    """Error parsing trip details."""
    pass


class NoTripDetails(AIMSException):
    """AIMS unable to find trip details"""
    pass


class BadCrewList(AIMSException):
    """Crew list parse failed."""
    pass


class BadAIMSSector(AIMSException):
    """Failed to process AIMS sector"""
    pass


class BadAIMSDuty(AIMSException):
    """Failed to process AIMS duty"""
