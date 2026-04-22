from src.extract.avelia_data_extraction import extract_avelia_data
from src.extract.iata_data_extraction import extract_iata_data
from src.extract.iscc_data_extraction import extract_iscc_data
from src.extract.rsb_data_extraction import extract_rsb_data
from src.extract.safc_data_extraction import extract_safc_data

def load_all():
    avelia_df = extract_avelia_data()
    iata_df = extract_iata_data()
    iscc_df = extract_iscc_data()
    rsb_df = extract_rsb_data()
    safc_df = extract_safc_data()
    
    return avelia_df, iata_df, iscc_df, rsb_df, safc_df

if __name__ == "__main__":
    load_all()