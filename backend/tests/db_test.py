import db
from freezegun import freeze_time

def test_recent_contributions():
    entity_id = 1
    query = db.recent_contributions(entity_id)
    expected_query = """SELECT donations.id, donations.donor_firstname, donations.donor_lastname, donations.donor_addr1, donations.donor_city, donations.donor_state, donations.donor_zip, donations.donor_is_eligible_for_express_lane, donations.donor_email, donations.donor_phone, donations.created_at, donations.order_number, donations.contribution_form, donations.refcodes, donations.refcode, donations.recurring_period, donations.recurring_duration, donations.is_paypal, donations.is_mobile, donations.is_express, donations.with_express_lane, donations.express_signup, donations.unique_identifier, donations.status, donations.text_message_option, donations.custom_fields, donations.sequence, donations.entity_id, donations.committee_name, donations.amount, donations.paid_at, donations.lineitem_id, donations.form_name, donations.form_managing_entity_name, donations.form_managing_entity_committee_name \nFROM donations \nWHERE donations.entity_id = :entity_id_1 ORDER BY donations.created_at DESC\n LIMIT :param_1"""
    assert str(query) == expected_query

def test_aggregate_contributions_by_day():
    entity_id = 1
    days = 10
    query = db.aggregate_contributions(entity_id, days)
    expected_query = """SELECT sum(donations.amount) AS sum_1 \nFROM donations \nWHERE donations.entity_id = :entity_id_1 AND donations.created_at >= :created_at_1 GROUP BY donations.entity_id"""
    assert str(query) == expected_query

@freeze_time("2022-10-10")
def test_start_date():
    start_date = db.start_date(7)
    assert start_date == "2022-10-03 00:00:00"