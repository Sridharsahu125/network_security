import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging 

# Load environment variable
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient='records')  # FIXED
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def insert_data_mongodb(self, record, database, collection):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = self.mongo_client[database]
            collection_obj = db[collection]
            collection_obj.insert_many(record)
            return len(record)
        except Exception as e:
            raise NetworkSecurityException(e, sys)   
        
if __name__=='__main__':
    FILE_PATH = "network_data\\phisingData.csv"
    DATABASE = "siriAI"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)

    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"Total Records Inserted: {no_of_records}")

                  