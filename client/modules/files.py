import os
import sys
import random
import server

def rewrite_file(filepath, max_lines, buffer, just_return=False):
    # Check if file exists
    if not os.path.exists(filepath):
        return f"Error: file '{filepath}' does not exist"

    # Check if file is not binary
    if not os.path.isfile(filepath):
        return f"Error: '{filepath}' is not a file"

    # Check if max_lines is valid
    if max_lines < 1:
        return "Error: max_lines must be greater than or equal to 1"

    # Check if buffer is smaller than max_lines
    if buffer >= max_lines:
        return "Error: buffer must be less than buffer"

    # Read the lines in the file
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Check if the file has enough lines
    if len(lines) <= max_lines:
        return f"Error: file '{filepath}' has less than {max_lines} lines"

    # Get the header line and last max_lines lines
    header_line = lines[0]
    # buffer gives us more time. we dont want everytime to rewrite file
    last_lines = lines[-(max_lines - buffer):]

    if just_return:
        return [header_line] + last_lines
    else:
        # Truncate the file and write the new data
        with open(filepath, 'w') as f:
            f.write(header_line)
            f.writelines(last_lines)

    return f"File '{filepath}' rewritten with {max_lines} lines"

def parse_logs(
        LOGS_DIR,
        READ_LINES,
        STORE_MAX_LINES,
        BUFFER_STORE_MAX_LINES,
        HOST,
        PORT,
        DEVICE_ID,
        JWT_SECRET,
        SERVER_CERTIFICATE
):
    # Check if the LOGS_DIR exists
    if not os.path.isdir(LOGS_DIR):
        print(f"Error: {LOGS_DIR} does not exist.")
        exit(1)

    data = {}
    # Read the last 100 lines of text files in the LOGS_DIR
    for filename in os.listdir(LOGS_DIR):
        filepath = os.path.join(LOGS_DIR, filename)
        if os.path.isfile(filepath) and filename.endswith(".txt"):
            if f"{filename}" not in data:
                data[f"{filename}"] = {
                    "header": [],
                    "data": []
                }
            with open(filepath, "r") as f:
                all_lines = f.readlines()

                header = all_lines[:1]
                data[f"{filename}"]["header"] = header[0].strip().split("\t")
                # throw some random value that we are going to ignore in server
                data[f"{filename}"]["header"].append("junk")
                lines = all_lines[-READ_LINES:]
                for i, line in enumerate(lines[1:]):
                    # throw some random value that we are going to ignore in server
                    junk = random.randint(99999, 99999999999)
                    values = line.strip().split("\t")
                    values.append(junk)
                    data[f"{filename}"]["data"].append(values)

            #trim file
            result = rewrite_file(filepath, STORE_MAX_LINES, BUFFER_STORE_MAX_LINES)

    response = server.send_data_to_server(HOST, PORT, DEVICE_ID, JWT_SECRET, data, SERVER_CERTIFICATE)

    print(response)
