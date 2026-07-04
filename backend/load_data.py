#%%
import pandas as pd 
import os 
import sys 
from dotenv import load_dotenv
from sqlalchemy import create_engine, types

#%%
#Load environment variables
#load csv 
load_dotenv(override=True)
csv_path = os.getenv("MARKETS_DATA_PATH")
db_url = os.getenv("DATABASE_URL")

try: 
    df = pd.read_csv(csv_path)
except Exception: 
    sys.exit("stopping execution")


# %%
df.head()

#%%


