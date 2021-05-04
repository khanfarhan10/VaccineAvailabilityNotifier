import requests
import datetime
import pandas as pd

#lists of district codes in india
did = []
dname = []
for state_code in range(1,40):
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
    res = response.json()
    for d in res['districts']:
        did.append(d['district_id'])
        dname.append(d['district_name'])
df = pd.DataFrame(list(zip(did,dname)), columns=['Did','Dname'])


numdays = 3
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

distid = []
date = []
pincode = []
state = []
l=34
for l in range(759):
    for INP_DATE in date_str:
        
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(df['Did'].iloc[l], INP_DATE)
        response = requests.get(URL)

        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                count = 0
                for k in resp_json["centers"]:
                    if k['sessions'][0]['min_age_limit'] == 18:
                        count += 1
                if(count>0):
                    distid.append(df['Dname'].iloc[l])
                    pincode.append(k["pincode"])
                    state.append(k["state_name"])
                    date.append(k['sessions'][0]['date'])
        l +=1
        if(l%20 == 0):
            print (l)

df2 = pd.DataFrame(list(zip(state,pincode,distid,date)), columns=['State',"Pincode",'Dist_name','Date'])
df2.to_csv("df2.csv")
