import typing as T
import datetime as DT
import enum


class SectorFlags(enum.Enum):
    POSITIONING = enum.auto()
    GROUND_DUTY = enum.auto()


class Sector(T.NamedTuple):
    start: DT.datetime
    finish: DT.datetime
    name: str
    from_: T.Optional[str]
    to: T.Optional[str]
    reg: T.Optional[str]
    flags: SectorFlags


class Duty(T.NamedTuple):
    start: DT.datetime
    finish: DT.datetime
    sectors: T.List[Sector]


class AIMSException(Exception):
    def __init__(self, str_: str ="") -> None:
        self.str_ = str_


class LogonError(AIMSException):
    """Logon failed."""
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
