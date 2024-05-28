import backend.main as main, db
import json
from pathlib import Path



### Make sure new_lineitem maps data keys onto db columns correctly
def test_new_lineitem():
    path = Path(__file__).parent / "./data/example_donation.json"
    with path.open() as f:
        d = json.load(f)
        lineitem = main.new_lineitem(d)
        
        donation_keys = db.Donation.__table__.columns.keys()
        assert list(lineitem.keys()) == donation_keys




