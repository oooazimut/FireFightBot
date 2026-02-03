from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Sprinkler:
    tank_level: float
    pressure: float
    crit_pressure: bool
    pump_is_running: bool
    sensor_fault: bool
    timestamp: datetime | None = None
