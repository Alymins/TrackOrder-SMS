import sqlite3
from track_order import send_msg, search_track_order


def save_track_code(save):
    db = sqlite3.connect("save/track_codes.db")
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS track_code(
track_id INTEGER PRIMARY KEY,
phone_number text not null,
code txt not null,
last_update text not null)""")
    has_code = c.execute("select 1 from track_code where code=?", (save[1],)).fetchone()
    has_phone_number = c.execute("select 1 from track_code where phone_number=?", (save[0],)).fetchone()
    if not (has_code and has_phone_number):
        c.execute('insert into track_code(phone_number, code, last_update) values (?,?,?)', save)
    db.commit()
    db.close()


def send_msg_every_day():
    db = sqlite3.connect("save/track_codes.db")
    c = db.cursor()
    data = c.execute("select * from track_code", ).fetchall()
    completed = []
    updates = []
    for dt in data:
        print(dt[2])
        result = search_track_order(dt[2])
        if result:
            if "entregue" in result['last_status']:
                completed.append(dt[0])
            if result["last_update"] != dt[3]:
                updates.append((dt[0], dt[1], result))
    for up in updates:
        send_msg(up[1], up[2])
        c.execute("UPDATE track_code SET last_update where track_id=?", (up[2]["last_update"], up[0]))
    for track_id in completed:
        c.execute('DELETE FROM track_code WHERE track_id=?', (track_id,))
    db.close()
