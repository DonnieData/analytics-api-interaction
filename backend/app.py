#%%
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv

#%%
load_dotenv()



#%%
#configure core application 
app = Flask(__name__)
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# %%
#pass database cconnecction 
#turns off a legacy modification tracking system
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initializing the extension - connection bewtwen database and flask app 
db = SQLAlchemy(app)
# %%

class FarmersMarket(db.Model):
    #assign class attributes 
    __tablename__ = 'NY_Farmers_Markets'
    __table_args__ = {'schema': 'public'}

    

# %%
