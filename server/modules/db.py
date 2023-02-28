import sqlite3
import sys


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
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id       INTEGER   PRIMARY KEY AUTOINCREMENT,
                device   INT       REFERENCES devices (id),
                type     CHAR (20),
                ts       INT,
                value    REAL,
                lat      REAL,
                lot      REAL,
                accuracy REAL,
                CONSTRAINT unique_type_ts UNIQUE (type, ts)
            );
''')
        conn.commit()
        conn.close()

    def update_devices(self, devices):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for device, device_data in devices.items():
            # Insert or update the device with description and state
            c.execute('INSERT INTO devices (device, description, state) VALUES (?, ?, ?) '
                      'ON CONFLICT (device) DO UPDATE SET description = excluded.description, state = TRUE',
                      (device_data['id'], device_data['description'], True))
        conn.commit()
        conn.close()

    def add_data(self, device, data):
        result = {
            'status': True,
            'message': ''
        }
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute('SELECT * FROM devices WHERE device = ?', (f'{device}',))
        row = c.fetchone()
        if row:
            device_id, device, description, state = row
            if state:
                sql_data = []
                for log_type, log_data in data.items():
                    type = log_type.split('_')[0]
                    if isinstance(log_data, dict):
                        temp_header = log_data["header"]
                        header = []
                        for header_name in temp_header:
                            if header_name.startswith('lat'):
                                header_name = 'lat'
                            if header_name.startswith('lon'):
                                header_name = 'lon'
                            if header_name.startswith('accuracy'):
                                header_name = 'accuracy'
                            if header_name.startswith('Unix timestamp'):
                                header_name = 'ts'
                            header.append(header_name)

                        for data_row in log_data["data"]:
                            temp_data = [device_id, type]
                            header_index = -1
                            for header_name in header:
                                header_index += 1
                                if header_name != 'unit' and header_name != 'junk':
                                    if header_name == 'ts':
                                        temp_data.append(int(data_row[header_index]))
                                    elif header_name != 'value':
                                        temp_data.append(float(data_row[header_index]))
                                    else:
                                        temp_data.append(round(float(data_row[header_index]), 2))

                            sql_data.append(temp_data)

                c.executemany(
                    'INSERT OR IGNORE INTO sensor_data (device, type, ts, value, lat, lot, accuracy) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?) ',
                    sql_data
                )
                conn.commit()
                conn.close()
            else:
                result['status'] = False
                result['message'] = "Invalid device"
        else:
            result['status'] = False
            result['message'] = "Invalid device"

        return result
