import os
import sys
import struct
from decouple import config


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

WORLDCUP_LOGS_DIRECTORY = config("worldcup_logs_directory", default=CURRENT_DIR)
if WORLDCUP_LOGS_DIRECTORY[-1] == "/":
    WORLDCUP_LOGS_DIRECTORY = WORLDCUP_LOGS_DIRECTORY[:-1]


struct_fmt = '!4I4B'
struct_len = struct.calcsize(struct_fmt)
struct_unpack = struct.Struct(struct_fmt).unpack_from


def get_timestamp_from_record(record):
    return record[0]


def process_file(file_name):
    with open(file_name, "rb") as f:
        requests = []
        data = f.read(struct_len)
        s = struct_unpack(data)
        current_dt = get_timestamp_from_record(s)
        count_per_second = 1

        while True:
            data = f.read(struct_len)
            if not data:
                requests.append(count_per_second)
                break
            s = struct_unpack(data)
            dt = get_timestamp_from_record(s)

            if dt != current_dt:
                diff = dt - current_dt - 1
                current_dt = dt
                requests.append(count_per_second)
                for _ in range(diff):
                    requests.append(0)
                count_per_second = 1
            else:
                count_per_second += 1
    return requests


if __name__ == "__main__":
    requests = []
    for i in range(5, 93):
        for j in range(1, 12):
            file_path = f"{WORLDCUP_LOGS_DIRECTORY}/wc_day{i}_{j}"
            if not os.path.exists(file_path):
                break
            requests.extend(process_file(file_path))
        print("processed day {}".format(i))

    if len(requests) == 0:
        print(f"No file found in the {WORLDCUP_LOGS_DIRECTORY}")
        sys.exit(0)
    print(len(requests) / 60 / 60 / 24)
    print("maximum requests in a second", sorted(requests, reverse=True)[:100])
    with open(f"{CURRENT_DIR}/workload.txt", "w") as f:
        for count in requests:
            f.write(f"{count} ")
    os.system(f"tar -jcvf {CURRENT_DIR}/workload.tbz2 {CURRENT_DIR}/workload.txt")
