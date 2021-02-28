import re
import pandas as pd
import numpy as np
import datetime
import sys
from pathlib import Path

file = open(sys.argv[1], 'r')
Path("output").mkdir(parents=True, exist_ok=True)
 

logs_entries = []

for entry in file:
    line = re.compile(r'^((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(sshd)\S+:\s+(.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*)$').search(entry)
    if line:
        datetime_str = line.group(1) + " " + str(datetime.datetime.now().year)
        datetime_obj = datetime.datetime.strptime(datetime_str, '%b %d %H:%M:%S %Y')
        logs_entries.append({"hostname": line.group(3), "ip_address": line.group(6), "date_time": datetime_obj, "message": line.group(5)})

df = pd.DataFrame(logs_entries)
df.sort_values(by=['ip_address'], ascending=True, inplace=True, kind='mergesort')
df["hostname"] = df["hostname"].mask(df["hostname"].duplicated())
df["ip_address"] = df["ip_address"].mask(df["ip_address"].duplicated())
df.to_excel("output/access_log_formatted.xlsx")
file.close()