from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import IntEnum
import json
from typing import Callable, List

from domain.models import Facility, Pump, Tank


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


def to_domain_model(registers: List, to_float: Callable) -> Facility:
    mask = registers[Registers.MASK]
    level = registers[Registers.LEVEL]
    tank = Tank(level=100 if 200 > level > 100 else level)
    pump = Pump(
        pressure=to_float(registers[PRESSURE]),
        is_working=get_bit(mask, Bits.RUN),
        crit_pressure=get_bit(mask, Bits.CRIT_PRESSURE),
    )

    return Facility(datetime.now(), tank, pump, get_bit(mask, Bits.SENSOR_FAULT))


def to_json(obj) -> str:
    def selialize(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Type {type(o)} not selializeble")

    if is_dataclass(obj):
        return json.dumps(asdict(obj), default=selialize)
    else:
        raise TypeError("Object is not dataclass")
