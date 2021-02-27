import re
import pandas as pd
import numpy as np
import datetime
import ipaddress
import requests

file = open("logfile.log", 'r')


logs_entries = []

for entry in file:
    line = re.compile(
        r'^((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(sshd)\S+:\s+(.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*)$').search(entry)
    if line:
        datetime_str = line.group(1) + " " + str(datetime.datetime.now().year)
        datetime_obj = datetime.datetime.strptime(
            datetime_str, '%b %d %H:%M:%S %Y')
        logs_entries.append({"hostname": line.group(3), "ip_address": line.group(
            6), "date_time": datetime_obj, "message": line.group(5)})

df = pd.DataFrame(logs_entries)
df.sort_values(by=['ip_address'], ascending=True,
               inplace=True, kind='mergesort')
ips = list(set(list(df["ip_address"])))
geoip_dict = []
for ip in ips:
    print(ip)
    if ipaddress.ip_address(ip).is_global:
        response = requests.get(
            f"https://api.ipgeolocation.io/ipgeo?apiKey=64c265c69b3348f784d5ea0c407269b0&ip={ip}")
        response_body = response.json()
        geoip_dict.append({"ip_address": ip, "country": response_body["country_name"], "city": response_body["city"],
                           "isp": response_body["isp"], "latitude": response_body["latitude"], "longitude": response_body["longitude"]})
    else:
        geoip_dict.append({"ip_address": ip, "country": None, "city": None, "isp": None, "latitude": None, "longitude": None})

hdf = pd.DataFrame(geoip_dict)
result = pd.merge(hdf, df, how="right", on=["ip_address"])
result = result[["hostname", "ip_address", "country", "city",
                 "isp", "latitude", "longitude", "date_time", "message"]]
result["hostname"] = result["hostname"].mask(result["hostname"].duplicated())
result["ip_address"] = result["ip_address"].mask(
    result["ip_address"].duplicated())
result["country"] = result["country"].mask(result["country"].duplicated())
result["city"] = result["city"].mask(result["city"].duplicated())
result["isp"] = result["isp"].mask(result["isp"].duplicated())
result["latitude"] = result["latitude"].mask(result["latitude"].duplicated())
result["longitude"] = result["longitude"].mask(
    result["longitude"].duplicated())
result.to_excel("output_formatted_geoip.xlsx")
file.close()
