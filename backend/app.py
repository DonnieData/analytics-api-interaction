#%%
import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime 
from zoneinfo import ZoneInfo
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
        market_raw = [i.to_dict() for i in market_data]
        df = pd.DataFrame(market_raw)
        df = df.fillna("")

        #format needed to convert properly and dispaly on front end 
        #formats it exactly how forntend javasccript and plotly needs
        market_json = df.to_dict(orient="records")
        return jsonify(market_json)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/v1/markets/summary-by-county", methods=["GET"])
def get_county_summary_sql():
    try:

        summary_data = db.session.query(FarmersMarket.county,
            func.count(FarmersMarket.id).label('market_count')
            ).group_by(FarmersMarket.county).order_by(func.count(
            FarmersMarket.id).desc()).all()
        
        #format tuples 
        records = []
        for county, count in summary_data:
            # Handle null values defensively and standardize casing
            clean_county = county.strip().upper() if county else "UNKNOWN"
            
            records.append({
                "county": clean_county,
                "market_count": count
            })

        return jsonify(records)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/v1/markets/market-geo-plot", methods=["GET"])
def get_geo_scatter():
    try:
        results = db.session.query(
            FarmersMarket.market_name,
            FarmersMarket.operation_hours,
            FarmersMarket.latitude,
            FarmersMarket.longitude
            ).filter(FarmersMarket.latitude.isnot(None), FarmersMarket.longitude.isnot(None)).all()

        payload = [
            {
                "name": i.market_name,
                "hours": i.operation_hours if i.operation_hours else "Hours not listed",
                "lat": float(i.latitude),
                "lon": float(i.longitude)
            }
            for i in results
            ]
        
        return jsonify(payload)
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#---------------------------------------------------
#Layout / UI ENTRY ROUTE 

#route to display front end which will serve ui to interact with other api endpoints
@app.route("/layout", methods=["GET"])
def app_layout():
    """Serves the interactive frontend"""

    # get and serve eastern time 
    eastern_tz = ZoneInfo("America/New_York")
    now_eastern = datetime.now(eastern_tz)
    formatted_time = now_eastern.strftime("%B %d, %Y — %I:%M %p %Z")
    return render_template("layout.html", current_time=formatted_time)
# %%
if __name__ == "__main__":
    app.run(debug=True, port=5000)
# %%
