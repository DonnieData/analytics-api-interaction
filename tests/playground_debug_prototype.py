
#debugging with interactive cellsin VSCode with jupyter magic
#%%
import sys
import os 
import pprint
from flask import jsonify

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
    market = db.session.query(FarmersMarket).limit(10).all()

    market_j = [i.to_dict() for i in market]
    #market_j = jsonify(market_j)
    pprint.pprint(market_j)
    #print(market.to_dict())
    #pprint.pprint(market.__dict__)
    #print(market.__dict__)
    #for i in market:
     #   print (i.to_dict())
      #  print("/n")
# %%
#dir(market)
# %%s
FarmersMarket

# %%


# %

# %%
