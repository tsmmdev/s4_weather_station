import sqlite3
# import sys


class WeatherDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
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
                CONSTRAINT unique_device_type_ts UNIQUE (device, type, ts)
            );
''')
        c.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_sensor_data_type_ts
    ON sensor_data (type, ts)
''')
        conn.commit()
        conn.close()

    def update_devices(self, devices):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for device, device_data in devices.items():
            # Check if device already exists in database
            c.execute('SELECT id FROM devices WHERE device = ?', (device_data['id'],))
            result = c.fetchone()
            if result:
                # Device already exists, update its description and state
                c.execute('UPDATE devices SET description = ?, state = TRUE WHERE id = ?',
                          (device_data['description'], result[0]))
            else:
                # Device does not exist, insert it with description and state
                c.execute('INSERT INTO devices (device, description, state) VALUES (?, ?, ?)',
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
                sql_data = {}
                for log_type, log_data in data.items():
                    data_type = log_type.split('_')[0]
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
                            if data_type not in sql_data:
                                sql_data[data_type] = []
                            temp_data = [device_id, data_type]
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

                            sql_data[data_type].append(temp_data)

                # for data_type in sql_data:
                for data_type, sql_dat in sql_data.items():
                    c.execute(
                        'SELECT ts FROM sensor_data WHERE device = ? AND type = ? ORDER BY ts DESC LIMIT 1',
                        (device_id, data_type)
                              )

                    ts_check = c.fetchone()
                    data_to_insert = sql_dat
                    if ts_check:
                        data_to_insert = []
                        biggest_ts = ts_check[0]

                        for sql_dat_row in sql_dat:
                            if sql_dat_row[2] > biggest_ts:
                                data_to_insert.append(sql_dat_row)

                    c.executemany(
                        'INSERT INTO sensor_data (device, type, ts, value, lat, lot, accuracy) '
                        'VALUES (?, ?, ?, ?, ?, ?, ?) ',
                        data_to_insert
                    )
                    # OR IGNORE
                conn.commit()
                conn.close()
            else:
                result['status'] = False
                result['message'] = "Invalid device"
        else:
            result['status'] = False
            result['message'] = "Invalid device"

        return result
