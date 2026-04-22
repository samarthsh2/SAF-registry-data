from datetime import datetime
import requests
import pandas as pd
import io

def extract_iata_data():    
    url = "https://safregistry.iata.org/pubassets/public_redemptions.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        "Accpet": "application/json, text/plain, */*"
    }

    response = requests.get(url, headers=headers, verify=False)

    df = pd.read_csv(io.BytesIO(response.content))  # reads bytes directly
    # df.drop(["safrId", "redemptionFormula", "tlce", "claimingScheme", "status", "emissionsStatementId", "historicalTransaction", "frozen", "redemptionFacilitator"], axis=1, inplace=True)
    # df['redemptionDate'] = pd.to_datetime(df["redemptionDate"]).dt.date

    return df
    # df.to_excel(f"./Data/IATA_SAF_Data_{datetime.now().strftime('%d%m%Y')}.xlsx", header=True)