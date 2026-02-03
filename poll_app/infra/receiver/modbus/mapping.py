from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import IntEnum
import json
from typing import Callable, List

from domain.models import Sprinkler


class Registers(IntEnum):
    LEVEL = 0
    MASK = -1


PRESSURE = slice(2, 4)


class Bits(IntEnum):
    RUN = 0
    CRIT_PRESSURE = 1
    SENSOR_FAULT = 2


def get_bit(mask: int, bit: int) -> bool:
    return bool(mask & (1 << bit))


def to_domain_model(registers: List, to_float: Callable) -> Sprinkler:
    mask = registers[Registers.MASK]
    level = registers[Registers.LEVEL]

    return Sprinkler(
        tank_level=100 if 200 > level > 100 else level,
        pressure=to_float(registers[PRESSURE]),
        crit_pressure=get_bit(mask, Bits.CRIT_PRESSURE),
        pump_is_running=get_bit(mask, Bits.RUN),
        sensor_fault=get_bit(mask, Bits.SENSOR_FAULT),
    )


def to_json(obj) -> str:
    if is_dataclass(obj):
        return json.dumps(asdict(obj))
    else:
        raise TypeError("Object is not dataclass")
