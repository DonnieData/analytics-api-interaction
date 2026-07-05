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
    df = pd.read_csv(csv_path, dtype={'Zip': str, 'Phone': str})
except Exception: 
    sys.exit("stopping execution")


# %%
#df.head()

#%%
# Clean column names (strip whitespace and replace spaces/punctuation with underscores)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#%%
# 3. Explicitly define and enforce PostgreSQL data types
dtype_mapping = {
    'county': types.VARCHAR(100),
    'market_name': types.VARCHAR(255),
    'market_location': types.TEXT,
    'address_line_1': types.VARCHAR(255),
    'city': types.VARCHAR(100),
    'state': types.VARCHAR(50),
    'zip': types.VARCHAR(10),       # Enforce varchar to preserve zip codes starting with 0
    'contact': types.VARCHAR(255),
    'phone': types.VARCHAR(20),       # Enforce varchar to prevent sci-notation or integer conversion
    'market_link': types.TEXT,
    'operation_hours': types.TEXT,
    'operation_season': types.TEXT,
    'operating_months': types.VARCHAR(50),
    'fmnp': types.VARCHAR(5),         # Holds 'Y' / 'N'
    'snap': types.VARCHAR(5),         # Holds 'Y' / 'N'
    'fcc_issued': types.VARCHAR(5),   # Holds 'Y' / 'N'
    'fcc_accepted': types.VARCHAR(5), # Holds 'Y' / 'N'
    'wic_vf': types.VARCHAR(5),       # Holds 'Y' / 'N'
    'latitude': types.Numeric(precision=9, scale=6),
    'longitude': types.Numeric(precision=9, scale=6),
    'georeference_1': types.TEXT
}

# %%
#establish connection paramter string 
#define table name 
engine = create_engine(db_url)
table_name ="NY_Farmers_Markets"

# %%

# %%
#connect to database and load 
try:
    print("attempting connection and bulk load")
    df.to_sql(
    name=table_name,
    con=engine,
    if_exists='replace',   # Options: 'fail', 'replace', or 'append'
    index=False,           # Don't create a separate column for the DataFrame index
    dtype=dtype_mapping,   # Enforce the strict PostgreSQL schema defined above
    chunksize=500,         # Pushes data in chunks for highly optimized memory usage
    method='multi'         # Bundles rows into multi-row INSERTs for fast loading
)
    print("bulk laod complete")
except OperationalError as e:
    # Catches connection timeouts, wrong passwords, or Neon database offline issues
    print(f"Database Connection Error during upload: {e}")

except SQLAlchemyError as e:
    # Catches SQL issues, such as type mapping conflicts or invalid table names
    print(f"SQLAlchemy error occurred while writing data: {e}")

except Exception as e:
    # Fallback for any other unexpected Python errors
    print(f"An unexpected error occurred: {e}") 

# %%
