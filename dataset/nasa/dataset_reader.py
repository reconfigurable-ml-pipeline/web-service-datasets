import os
import re
from datetime import datetime

from decouple import config


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

NASA_LOGS_DIRECTORY = config("nasa_logs_directory", default=CURRENT_DIR)
if NASA_LOGS_DIRECTORY[-1] == "/":
    NASA_LOGS_DIRECTORY = NASA_LOGS_DIRECTORY[:-1]


def get_timestamp_from_line(line):
    timestamp = re.search(r"[0-3][0-9]/(Aug|Jul)/1995:[0-2][0-9]:[0-6][0-9]:[0-6][0-9]", line)
    if timestamp:
        timestamp = timestamp.group()
    else:
        return None
    return timestamp


def process_file(file_name):
    with open(file_name, "r", encoding="ISO-8859-1") as f:
        line = f.readline()
        requests = []
        current_dt = datetime.strptime(get_timestamp_from_line(line), "%d/%b/%Y:%H:%M:%S")
        count_per_second = 0
        while line:
            timestamp = get_timestamp_from_line(line)
            if timestamp is None:
                line = f.readline()
                continue

            try:
                dt = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S")
            except ValueError:
                line = f.readline()
                continue

            if dt != current_dt:
                diff = int((dt - current_dt).total_seconds()) - 1
                current_dt = dt
                requests.append(count_per_second)
                for _ in range(diff):
                    requests.append(0)
                count_per_second = 1
            else:
                count_per_second += 1
            line = f.readline()
    return requests


if __name__ == "__main__":
    pass
    requests = process_file(f"{NASA_LOGS_DIRECTORY}/NASA_access_log_Jul95")
    requests.extend(process_file(f"{NASA_LOGS_DIRECTORY}/NASA_access_log_Aug95"))
    print("maximum requests in a second", sorted(requests, reverse=True)[:100])
    with open(f"{CURRENT_DIR}/workload.txt", "w") as f:
        for count in requests:
            f.write(f"{count} ")
    os.system(f"tar -jcvf {CURRENT_DIR}/workload.tbz2 {CURRENT_DIR}/workload.txt")
