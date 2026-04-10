from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import json
import requests
import pandas as pd
from datetime import datetime

opts = Options()
opts.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
opts.set_capability("ms:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

driver = webdriver.Edge(options=opts)
driver.get("https://registry.iscc-system.org/")
time.sleep(4)

logs = driver.get_log("performance")

for log in logs:
    log_message = json.loads(log.get("message"))
    if log_message.get("message").get("method") == "Network.requestWillBeSentExtraInfo":
        headers = log_message.get("message").get("params").get("headers")
        if headers.get("x-csrf-token", "") != "":
            break

driver.quit()

payload = {
    "action": "retrieve_by_xpath",
    "params": {
        "xpath": "//PublicArea.PublicTransactions",
        "schema": {
            "id": "b08d6dfb-4771-4ff7-8aaa-fa45fde1552b",
            "offset": 0,
            "sort": [["Date", "desc"]],
        },
        "count": True,
    },
    "profiledata": {
        "1775803815158-4": 354,
        "1775803815178-5": 650,
        "1775803860665-6": 283,
        "1775803860949-7": 228,
    },
}

response = requests.post(
    "https://registry.iscc-system.org/xas/", headers=headers, verify=False, json=payload
)
iscc_data = response.json().get("mxobjects", {})

required_data = []

for data in iscc_data:
    temp = {}
    temp["id"] = data["guid"]
    for key, values in data.get("attributes").items():
        temp[key] = values["value"]

    required_data.append(temp)


df = pd.DataFrame(required_data)
df['Date'] = pd.to_datetime(df['Date'], unit='ms').dt.date
df.drop(['Category', 'TransactionID', 'InformationSAFIncentivesUsed'], axis=1, inplace=True)

df.to_excel(f"./Data/ISCC_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)