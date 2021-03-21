import mariadb
import sys

try:
    conn = mariadb.connect(
        user="oscar",
        password="P2swVy7jvr",
        host="127.0.0.1",
        port=3306,
        database="Network"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()
line = "1|1|21"
cur.execute("SELECT * FROM IP_and_MAC")
for id, ip_address, mac_address in cur:
    print(f"{id}|{ip_address}|{mac_address}")
    line2 = f"{id}|{ip_address}|{mac_address}"
print(line2.find("21"))
conn.commit()
print(f"Last Inserted ID: {cur.lastrowid}")
conn.close()
