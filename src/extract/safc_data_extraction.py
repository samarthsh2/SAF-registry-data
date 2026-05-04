import requests
import pandas as pd
import urllib3


def extract_row(data: dict) -> dict:
    computed = data.get("computed", {})
    metadata = data.get("metadata", {})
    unit_type = computed.get("unitType", "")

    if unit_type == "SAFcE":
        beneficiary = get_beneficiary(metadata.get("sercClaimBeneficiary", {}))
        scope = 3
    else:
        beneficiary = get_beneficiary(metadata.get("safcClaimBeneficiary", {}))
        scope = 1

    return {
        "id": data.get("id"),
        "retiredAt": computed.get("retiredAt", {}).get("value"),
        "safcClaimBeneficiary": beneficiary,
        "Scope": scope,
        "SAFMetricTonnes": data.get("volume", 0),
        "co2Abated": computed.get("co2Abated"),
    }


def get_beneficiary(source: dict) -> str:
    if "name" in source:
        return source["name"].get("value", "")
    return source.get("ownerId", {}).get("value", "")


def extract_safc_data():
    url = "https://safcregistry.org/api/public/units/"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
        ),
    }
    params = {
        "type": "Claim",
        "sortBy": "retiredAt",
        "order": "desc",
        "limit": 50,
        "offset": 0,
    }
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    saf_data = []
    while True:
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        items = response.json().get("items", [])
        if not items:
            break
        saf_data.extend(items)
        params["offset"] = len(saf_data)

    dataset = pd.DataFrame([extract_row(d) for d in saf_data])
    return dataset
    # df.to_excel(f"./Data/SAFc_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)
