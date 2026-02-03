from contextlib import asynccontextmanager
from dataclasses import asdict
from psycopg.rows import AsyncRowFactory, class_row
from psycopg_pool import AsyncConnectionPool

from domain.models import Sprinkler
from domain.ports import SprinklerRepo


class PGBaseRepo:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool
        self._row_factory: AsyncRowFactory | None = None

    @asynccontextmanager
    async def _cursor(self):
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=self._row_factory) as cur:
                yield cur

    async def _execute(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)

    async def _fetchone(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)
            return await cur.fetchone()

    async def _fetchall(self, stmt, params=None):
        async with self._cursor() as cur:
            await cur.execute(stmt, params)
            return await cur.fetchall()


class PGSprinklerRepo(PGBaseRepo, SprinklerRepo):
    def __init__(self, pool: AsyncConnectionPool) -> None:
        super().__init__(pool)
        self.row_factory = class_row(Sprinkler)

    async def add(self, data: Sprinkler):
        stmt = """
        INSERT INTO sprinkler (tank_level, pressure, crit_pressure, pump_is_running, sensor_fault)
        VALUES (%(tank_level)s, %(pressure)s, %(crit_pressure)s, %(pump_is_running)s, %(sensor_fault)s)
        RETURNING tank_level, pressure, crit_pressure, pump_is_running, sensor_fault
        """
        return await self._fetchone(stmt, asdict(data))
