from pathlib import Path

import psycopg

from config import settings


async def init_db():
    script_path = Path(__file__).resolve().parent / "table.sql"
    user = settings.pg.user
    passwd = settings.pg.passw.get_secret_value()
    host = settings.pg.host
    db = settings.pg.db_name
    DSN = f"postgresql://{user}:{passwd}@{host}/{db}"

    async with await psycopg.AsyncConnection.connect(DSN) as conn:
        async with conn.cursor() as cur:
            with open(script_path, "r", encoding="utf-8") as file:
                await cur.execute(file.read())
        await conn.commit()
