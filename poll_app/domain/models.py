from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Pump:
    pressure: float
    is_working: bool
    crit_pressure: bool


@dataclass(frozen=True)
class Tank:
    level: float


@dataclass(frozen=True)
class Facility:
    timestamp: datetime
    tank: Tank
    pump: Pump
    sensor_fault: bool
