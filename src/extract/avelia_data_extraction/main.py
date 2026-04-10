import requests
import json
import pandas as pd
from datetime import datetime

URL = "https://www.aveliasolutions.com/publicservice/retirement/search"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}

response = requests.post(URL, headers=HEADERS)
data = json.loads(response.content)["docs"]
df = pd.DataFrame(data)

new_column_names = {
    '_id': "id",
    'blockchainTxnId': "Blockchain ID",
    'retirementDate': "Retirement Date Time",
    'allocatedSafVolumeGallons': "SAF Volume",
    'scope': "Scope",
    'companyName': "Retirement Beneficiary",
    'mtCo2': "GHG Abatement"
}

df.rename(columns=new_column_names, inplace=True)
df.drop(["allocationId", "carbonIntensity", "batchType", "publicRetirmentSetting"], inplace=True, axis=1)
df['Retirement Date Time'] = pd.to_datetime(df['Retirement Date Time'])
df['Retirement Date'] = df['Retirement Date Time'].dt.date
df.drop(['Retirement Date Time'], axis=1, inplace=True)

df.to_excel(f"./Data/Avelia_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)