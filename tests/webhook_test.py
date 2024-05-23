from backend import webhook, db
import json

### Make sure new_lineitem maps data keys onto db columns correctly
def test_new_lineitem():
    with open('example_donation.json') as f:
        d = json.load(f)
        lineitem = webhook.new_lineitem(d)
        
        donation_keys = db.Donation.metadata.columns.keys()
        assert lineitem.keys() == donation_keys




