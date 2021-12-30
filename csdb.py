import sqlite3
import items
from itertools import chain
import functions

# Registration DB
db = sqlite3.connect('DB/catalog.db')
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS items (
    id INTEGER AUTO_INCREMENT,
    item_id BIGINT UNIQUE,
    name TEXT,
    cost_down REAL,
    cost_up REAL,
    photo TEXT,
    description TEXT,
    weight REAL
)''')

db.commit()

for item in functions.my_iterator(items.items):
    sql.execute(f"SELECT item_id FROM items WHERE item_id = {item[0]}")
    if sql.fetchone() is None:
        if len(item) == 6:
            item.insert(3, item[2])
        sql.execute(f"INSERT INTO items (item_id, name, cost_down, cost_up, photo, description, weight) "
                    f"VALUES (?, ?, ?, ?, ?, ?, ?)", item)
        db.commit()
