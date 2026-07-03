#%%
import os 
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

#%%
load_dotenv(".env")  # Load environment variables from the .env file
db_conn_str = os.getenv("DATABASE_URL")  # Retrieve the connection string from environment variables
#print (db_conn_str)
 

# %%

conn = psycopg2.connect(db_conn_str)
#%%
multiple_rows = [
    (5, "Sofia", "Buenos Aires", 6, datetime.now()),
    (6, "Mateo", "Mexico City", 7, datetime.now())
]
 
# %%
with psycopg2.connect(db_conn_str, connect_timeout=5) as conn:
    with conn.cursor() as cur:
        multi_command_query = """
          CREATE SCHEMA IF NOT EXISTS test_analytics;

          CREATE TABLE IF NOT EXISTS test_analytics.tabla_prueba (
            id int,
            nombre varchar(50),
            ciudad varchar(50),
            dia int,
            marca_de_tiempo timestamp                 
                    );       
            INSERT INTO test_analytics.tabla_prueba (id, nombre, ciudad, dia, marca_de_tiempo) 
            VALUES 
                (5, 'Sofia', 'Buenos Aires', 6, NOW()),
                (6, 'Mateo', 'Mexico City', 7, NOW());
                        
            """
        cur.execute(multi_command_query)

        

# %%
with psycopg2.connect(db_conn_str, connect_timeout=5) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM test_analytics.tabla_prueba;")
        
        # This assigns the list of tuples to your variable
        my_data = cur.fetchall()

# You can now use the 'my_data' variable outside the database connection block
print(my_data)
# %%
