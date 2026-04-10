import requests
import pandas as pd
from datetime import datetime

url = "https://safcregistry.org/api/public/units/"
params = {"type":"Claim",
          "sortBy":"retiredAt",
          "offset": 0,
          "limit": 50,
          "order": "desc"}
headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}

saf_data = []
while True:
    response = requests.get(url, headers=headers, verify=False, params=params)
    data = response.json().get("items")
    if data != []:
        saf_data += data
        params['offset'] = len(saf_data)
    else:
        break

required_data = []
for data in saf_data:
    temp = {}
    temp["retiredAt"] = data.get("computed").get("retiredAt").get("value")
    if data.get("computed").get("unitType") == "SAFcE":
        if "name" in data.get("metadata").get("sercClaimBeneficiary").keys():
            temp["safcClaimBeneficiary"] = data.get("metadata").get("sercClaimBeneficiary").get("name").get("value")
        else:
            temp["safcClaimBeneficiary"] = data.get("metadata").get("sercClaimBeneficiary").get("ownerId").get("value")
        temp["Scope"] = 3
    else:
        if "name" in data.get("metadata").get("safcClaimBeneficiary").keys():
            temp["safcClaimBeneficiary"] = data.get("metadata").get("safcClaimBeneficiary").get("name").get("value")
        else:
            temp["safcClaimBeneficiary"] = data.get("metadata").get("safcClaimBeneficiary").get("ownerId").get("value")
        temp["Scope"] = 1
    temp["id"] = data.get("id")
    temp["SAFMetricTonnes"] = data.get("computed").get("rootMetadata").get("product").get("quantityMT").get("value")
    temp['co2Abated'] = data.get("computed").get("co2Abated")
    required_data.append(temp)

df = pd.DataFrame(required_data)
df['retiredAt'] = pd.to_datetime(df['retiredAt']).dt.date

df.to_excel(f"./Data/SAFc_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)