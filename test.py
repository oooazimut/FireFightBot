import sqlite3 as sq


with sq.connect('FireFight.db') as conn:
    conn.execute('delete from pressures')
    conn.commit()
