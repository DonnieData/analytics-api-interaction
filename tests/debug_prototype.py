
#debugging with interactive cells 
#%%
import sys
import os 
import pprint

#%%
sys.path.append("..")
os.listdir()
# %%
from app import app, db, FarmersMarket, db_url 
# %%
# %%
#flask feeature to immitate app running - to run query 
with app.app_context():
    #db.session.remove() to prevent errors when testing
    db.session.remove()
    market = db.session.query(FarmersMarket).first()

    pprint.pprint(market.__dict__)
# %%
#dir(market)
# %%s
FarmersMarket

# %%


# %

# %%
