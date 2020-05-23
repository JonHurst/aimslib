import typing as T
import datetime as DT
import enum


class CrewMember(T.NamedTuple):
    name: str
    role: str


class SectorFlags(enum.Flag):
    NONE = 0
    POSITIONING = enum.auto()
    GROUND_DUTY = enum.auto()
    QUASI = enum.auto()
    # QUASI means a standby or SEP segment recorded in a duty as a sector


class Sector(T.NamedTuple):
    name: str
    from_: T.Optional[str]
    to: T.Optional[str]
    sched_start: DT.datetime
    sched_finish: DT.datetime
    act_start: T.Optional[DT.datetime]
    act_finish: T.Optional[DT.datetime]
    reg: T.Optional[str]
    type_: T.Optional[str]
    flags: SectorFlags
    crewlist_id: T.Optional[str]


class TripID(T.NamedTuple):
    aims_day: str
    trip: str


class Duty(T.NamedTuple):
    trip_id: TripID
    start: T.Optional[DT.datetime]
    finish: T.Optional[DT.datetime]
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


class BadRosterEntry(AIMSException):
    """A RosterEntry object could not be converted."""
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
