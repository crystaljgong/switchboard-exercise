from sqlalchemy import Column, Integer, String, Boolean, Numeric, JSON, DateTime, func, select
from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

dbpath = (
    f"postgresql://{os.getenv('DB_USER')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(dbpath, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def insert_lineitem(lineitem):
    lineitem = Donation(**lineitem)
    session.add(lineitem)
    session.commit()

def execute_query(query):
    rows = session.execute(query).all()
    return rows

def recent_contributions(entity_id):
    query = select(Donation) \
        .where(Donation.entity_id == entity_id) \
        .order_by(Donation.created_at.desc()).limit(10)
    return query

def aggregate_contributions(entity_id, days=None):
    query = select(func.sum(Donation.amount)) \
        .where(Donation.entity_id == entity_id) \
        .group_by(Donation.entity_id)
    
    # Return return a subset of donations from the last n days
    if days:
        query = query.where(Donation.created_at >= start_date(days)) \
        
    return query

def filter_by_refcode(refcode, query):
    return query.where(Donation.refcode == refcode)

def start_date(days):
    start_date = datetime.today() - timedelta(days=days)
    return str(start_date)

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True)
    donor_firstname = Column(String(250))
    donor_lastname = Column(String(250))
    donor_addr1 = Column(String(250))
    donor_city = Column(String(250))
    donor_state = Column(String(50))
    donor_zip = Column(String(50))
    donor_is_eligible_for_express_lane = Column(Boolean)
    donor_email = Column(String(254))
    donor_phone = Column(String(128))
    created_at = Column(DateTime(timezone=True))
    order_number = Column(String(150))
    contribution_form = Column(String(150))
    refcodes = Column(JSON)
    refcode = Column(String(255))
    recurring_period = Column(String(50))
    recurring_duration = Column(String(50))
    is_paypal = Column(Boolean)
    is_mobile = Column(Boolean)
    is_express = Column(Boolean)
    with_express_lane = Column(Boolean)
    express_signup = Column(Boolean)
    unique_identifier = Column(String(75))
    status = Column(String(75))
    text_message_option = Column(String(75))
    custom_fields = Column(JSON)
    sequence = Column(Integer)
    entity_id = Column(Integer)
    committee_name = Column(String(150))
    amount = Column(Numeric(19, 4))
    paid_at = Column(DateTime(timezone=True))
    lineitem_id = Column(String(150))
    form_name = Column(String(150))
    form_managing_entity_name = Column(String(150))
    form_managing_entity_committee_name = Column(String(150))


