from fastapi import FastAPI
import db as db

from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/actblue_donation/")
async def actblue_donation(request: Request):
    data = await request.json()
    try:
        db.insert_lineitem(new_lineitem(data))
        return {"status": "successfully inserted lineitem"}
    except:
        return {"status": "failed to insert lineitem"}


@app.get("/recent_donations/entity/{entity_id}")
async def recent_donations(entity_id: int):
    try:
        query = db.recent_contributions(entity_id)
        rows = db.execute_query(query)
        data = [row[0].__dict__ for row in rows]
        return data
    except:
        return {"status": "failed to retrieve recent donations"}

@app.get("/aggregate_contributions/entity/{entity_id}/days/{days}")
async def aggregate_contributions(entity_id: int, days: int):
    try:
        query = db.aggregate_contributions(entity_id, days)
        rows = db.execute_query(query)
        return rows[0][0]
    except:
        return {"status": f"failed to retrieve aggregate contributions for entity {entity_id}"}

@app.get("/aggregate_contributions/entity/{entity_id}")
async def aggregate_contributions(entity_id: int):
    try:
        query = db.aggregate_contributions(entity_id)
        rows = db.execute_query(query)
        return rows[0][0]
    except:
        return {"status": f"failed to retrieve aggregate contributions for entity {entity_id}"}


def new_lineitem(data):
    donor = data["donor"]
    contribution = data["contribution"]
    lineitems = data["lineitems"][0]  # each donation has only one lineitem
    form = data["form"]
    lineitem = {
        "id": lineitems["lineitemId"],
        "donor_firstname": donor["firstname"],
        "donor_lastname": donor["lastname"],
        "donor_addr1": donor["addr1"],
        "donor_city": donor["city"],
        "donor_state": donor["state"],
        "donor_zip": donor["zip"],
        "donor_is_eligible_for_express_lane": donor["isEligibleForExpressLane"],
        "donor_email": donor["email"],
        "donor_phone": donor["phone"],
        "created_at": contribution["createdAt"],
        "order_number": contribution["orderNumber"],
        "contribution_form": contribution["contributionForm"],
        "refcodes": contribution["refcodes"],
        "refcode": contribution["refcode"],
        "recurring_period": contribution["recurringPeriod"],
        "recurring_duration": contribution["recurringDuration"],
        "is_paypal": contribution["isPaypal"],
        "is_mobile": contribution["isMobile"],
        "is_express": contribution["isExpress"],
        "with_express_lane": contribution["withExpressLane"],
        "express_signup": contribution["expressSignup"],
        "unique_identifier": contribution["uniqueIdentifier"],
        "status": contribution["status"],
        "text_message_option": contribution["textMessageOption"],
        "custom_fields": contribution["customFields"],
        "sequence": lineitems["sequence"],
        "entity_id": lineitems["entityId"],
        "committee_name": lineitems["committeeName"],
        "amount": lineitems["amount"],
        "paid_at": lineitems["paidAt"],
        "lineitem_id": lineitems["lineitemId"],
        "form_name": form["name"],
        "form_managing_entity_name": form["managingEntityName"],
        "form_managing_entity_committee_name": form["managingEntityCommitteeName"],
    }
    return lineitem
