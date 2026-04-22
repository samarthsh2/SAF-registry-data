import pandas as pd
import requests

def extract_rsb_data():

    url = "https://api.registry.rsb.org/v1/retirement-statements/public-list"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    page_size = 200  # try 200/500/1000 if API allows (bigger = fewer requests)

    session = requests.Session()
    session.headers.update(headers)

    # Use a timeout so Power BI doesn't hang forever on a slow call
    TIMEOUT = 30

    # First call to get total pages (or you can loop until empty without totalPages)
    first_params = {"page": 1, "pageSize": page_size}
    first_resp = session.get(url, params=first_params, verify=False, timeout=TIMEOUT)
    first_resp.raise_for_status()

    first_json = first_resp.json()
    total_pages = first_json["metadata"]["pagination"]["totalPages"]

    all_statements = first_json.get("data", [])

    # Fetch remaining pages correctly (page=2..total_pages)
    for page in range(2, total_pages + 1):
        params = {"page": page, "pageSize": page_size}
        resp = session.get(url, params=params, verify=False, timeout=TIMEOUT)
        resp.raise_for_status()

        page_data = resp.json().get("data", [])
        if not page_data:
            break

        all_statements.extend(page_data)

    # Flatten credits using list comprehension (faster than nested append loops)
    rows = [
        {
            "id": credit.get("RSID"),
            "issueDate": credit.get("issueDate"),
            "safAmountMT": credit.get("amount"),
            "companyNameforScope3": credit.get("scope3"),
            "companyNameforScope1": credit.get("scope1"),
        }
        for statement in all_statements
        for credit in (statement.get("credits") or [])
    ]

    df = pd.DataFrame(rows)


    return df
    # df.to_excel(f"./Data/RSB_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)