import sqlite3


class WeatherDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                device      CHAR (25)  UNIQUE,
                description CHAR (100),
                state       BOOLEAN    DEFAULT (TRUE)
            );
        ''')
        conn.commit()
        c.execute('''
            CREATE TABLE sensor_data (
                id       INTEGER   PRIMARY KEY AUTOINCREMENT,
                device   INT       REFERENCES devices (id),
                ts       INT,
                type     CHAR (20),
                value    REAL,
                lat      REAL,
                lot      REAL,
                accuracy REAL
            );
        ''')
        conn.commit()
        conn.close()

    def insert_or_update_devices(self, devices):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        for device in devices:
            # Check if the device exists in the database
            c.execute('SELECT id FROM devices WHERE device = ?', (device['device'],))
            result = c.fetchone()

            if result:
                # Update the device description
                c.execute('UPDATE devices SET description = ? WHERE id = ?', (device['description'], result[0]))
            else:
                # Insert a new device
                c.execute('INSERT INTO devices (device, description) VALUES (?, ?)',
                          (device['device'], device['description']))

        conn.commit()
        conn.close()
