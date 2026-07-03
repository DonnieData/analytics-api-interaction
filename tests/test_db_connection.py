#%%
import os 
import psycopg2
import sys
from dotenv import load_dotenv
from datetime import datetime

#%%
print("laoding environment vars")
load_dotenv(".env")  # Load environment variables from the .env file
db_conn_str = os.getenv("DATABASE_URL")  # Retrieve the connection string from environment variables
#print (db_conn_str)
 
if not db_conn_str:
    print("Error:database_url not  found")
    sys.exit("stopping execution")
# %%

conn = psycopg2.connect(db_conn_str)
#%%
multiple_rows = [
    (5, "Sofia", "Buenos Aires", 6, datetime.now()),
    (6, "Mateo", "Mexico City", 7, datetime.now())
]
 
# %%
try:
    with psycopg2.connect(db_conn_str, connect_timeout=5) as conn:
        print("database cconnection established successfully")
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
            print("execcuting queries")
            cur.execute(multi_command_query)
            print("queries executed succcessfully")
except psycopg2.OperationalError: 
    print("Connecction failed, check env credentilas")     

# %%
try: 
    with psycopg2.connect(db_conn_str, connect_timeout=5) as conn:
        print(" quering data")
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM test_analytics.tabla_prueba;")
            
            # This assigns the list of tuples to your variable
            my_data = cur.fetchall()
            print("results  retrieved")

except psycopg2.OperationalError as e:
    print(" connection failed ")
except psycopg2.DatabaseError as e:
    print("query failed")

#output data 
print(my_data)



# %%
