import pandas as pd
import requests
from datetime import datetime

url = "https://api.registry.rsb.org/v1/retirement-statements/public-list"
headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
payload = {
    "page": 1,
    "pageSize": 50
}

rsb_saf_data = []
while True:
    response = requests.get(url, headers=headers, verify=False, params=payload)
    data = response.json().get("data", [])
    if data == []:
        break
    rsb_saf_data += data
    payload['page'] = payload['page']+1
    
required_data = []
for data in rsb_saf_data:
    for credit in data.get("credits"):
        temp = {}
        temp['id'] = credit['RSID']
        temp['issueDate'] = credit['issueDate']
        temp['safAmountMT'] = credit['amount']
        temp['companyNameforScope3'] = credit['scope3']
        temp['companyNameforScope1'] = credit['scope1']       
        required_data.append(temp)

df = pd.DataFrame(required_data)
df['issueDate'] = pd.to_datetime(df['issueDate']).dt.date

df.to_excel(f"./Data/RSB_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)