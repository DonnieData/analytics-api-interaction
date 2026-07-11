#%%
import os
from flask import Flask, jsonify, request, render_template
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

#%%

# %%
#pass database cconnecction 
#turns off a legacy modification tracking system
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initializing the extension - connection bewtwen database and flask app 
db = SQLAlchemy(app)
# %%

#model/mapping of farmers market table within the ddatabase 
class FarmersMarket(db.Model):
    #assign class attributes/ table metadata 
    __tablename__ = 'NY_Farmers_Markets'
    __table_args__ = {'schema': 'public'}

    #define column mapping 
    #varaibles are  named exactly as they are in database 
    county = db.Column(db.String(100))
    market_name = db.Column(db.String(300))
    market_location = db.Column(db.Text)
    address_line_1 = db.Column(db.Text )
    city =  db.Column(db.String(100))
    state =  db.Column(db.String(100))
    zip =  db.Column(db.String(20))
    contact = db.Column(db.String(300))
    phone = db.Column(db.String(20))
    market_link = db.Column(db.Text)
    operation_hours = db.Column(db.Text)
    operation_season = db.Column(db.Text)
    operating_months = db.Column(db.Text)
    fmnp = db.Column(db.String(5))
    snap = db.Column(db.String(5))
    fcc_issued = db.Column(db.String(5))
    fcc_accepted = db.Column(db.String(5))
    wic_vf = db.Column(db.String(5))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    georeference_1 = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #%%
    #FarmersMarket.__tablename__
    #FarmersMarket.county
#%%
#helps map data so its intepretable and endpoint doesnt break
#Flask APIs communicate using JSON when database is queried using SQLAlchemy, it doesn't return a dictionary/JSON; returns a SQLAlchemy Model Instance (a object with database connections attached to it)
    def to_dict(self):
        return {
            "county": self.county ,
            "market_name": self.market_name ,
            "market_location": self.market_location ,
            "address_line_1": self.address_line_1 ,
            "city": self.city ,
            "state": self.state ,
            "zip": self.zip ,
            "contact": self.contact ,
            "phone": self.phone ,
            "market_link": self.market_link ,
            "operation_hours": self.operation_hours ,
            "operation_season": self.operation_season ,
            "operating_months": self.operating_months ,
            "fmnp_accepted": self.fmnp ,
            "snap_accepted": self.snap  ,
            "fcc_issued": self.fcc_issued ,
            "fcc_accepted": self.fcc_accepted ,
            "wic_vf": self.wic_vf ,
            "coordinates": {"lat": self.latitude, "lng": self.longitude},
            "georeference_1": self.georeference_1 ,
            "id": self.id 
            }

# %%

#---api endpoints 
# proof of concept endpoint
#deccorator,root, version, resource, action/identifier
@app.route("/api/v1/markets/test-ten", methods=["GET"])
def get_test_data():
    """endpoint returning first 10 rows"""

    try:
        market_data = db.session.query(FarmersMarket).limit(10).all()
        
        market_json = [i.to_dict() for i in market_data]

        return market_json

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/layout", methods=["GET"])
def app_layout():
    """Serves the interactive frontend"""
    return render_template("layout.html")
# %%
if __name__ == "__main__":
    app.run(debug=True, port=5000)
# %%
