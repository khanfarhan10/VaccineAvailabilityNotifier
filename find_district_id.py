"""
python find_district_id.py
"""

import requests
import datetime
import json
import csv
# import pandas as pd

columns=['StateCode','DistrictID','DistrictName']

with open('district_data.csv', mode='w') as fh:
  fwriter = csv.writer(fh, delimiter=',')
  fwriter.writerow(columns)
  for state_code in range(1,40):
    #print("State code: ", state_code)
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
    json_data = json.loads(response.text)
    for i in json_data["districts"]:
        #print(i["district_id"],'\t', i["district_name"])
        fwriter.writerow([state_code,i["district_id"], i["district_name"]])
    #print("\n")
