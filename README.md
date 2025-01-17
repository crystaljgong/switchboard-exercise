# Switchboard Engineering Exercise

This repository contains the back-end for an app that interfaces with Actblue donation data. 

The API contains an endpoint that can receive Actblue webhook donation data, as well as endpoints that display aggregates donation amounts for a given entity ID.

## Tech stack

Backend:
- FastAPI as the web framework
- sqlalchemy for the ORM
- postgres database

## Installation

### Database setup
You can use homebrew to install postgres
'''
brew install postgresql
'''
start the database with
'''
brew services start postgresql@15
'''

Download the `donations.sql` file from [the drive](https://drive.google.com/drive/folders/1P_YlH4yqYkhejWN088IjLl4cwLah6_5j) and insert it into the your database. 

`
psql -h hostname -p port_number -U username -f donations.sql dbname `

Your database should now have a table called `donations` with 17713 rows in it. 

Optionally set `lineitem_id` as the primary key. I did this via postico, a postgresql GUI.

### Environment setup
Create a `.env file`

```
cp .env.example .env
```

and replace the values your own DB user, name, host, and port.

### Installing the python dependencies

Make a virtual environment in python

```
python3 -m venv venv
```
and activate the virtual environment
```
source venv/bin/activate
```
Install the dependencies
```
pip install -r requirements.txt
```

## Running

### Running the backend

Run the server with 
```
uvicorn main:app --reload
```

Your backend server should now run at <http://localhost:8000>. 

### Testing

## Testing with pytest

Run `pytest` to run unit tests in `backend/tests`. 

## Testing with curl
Selecting items from the donation table with lineitem_id=600314606 returns one lineitem. 

![Selecting items in db with lineitem_id=600314606 before webhook request](image-1.png)

In a separate terminal from the one the server is running, send a curl request to the simulate a webhook from Actblue. 

NOTE: The lineitem number has been changed from `500314606` to `600314606` to avoid conflict with an existing lineitem with `id = 500314606`.

```
curl --location --request POST 'localhost:8000/actblue_donation/' --header 'Authorization: Basic YWN0Ymx1ZTpDSEFOR0VNRQ==' --header 'Content-Type: application/json' --data-raw '{
    "donor": {
        "firstname": "Shreyes",
        "lastname": "Seshasai",
        "addr1": "123 Main St",
        "city": "Washington",
        "state": "DC",
        "zip": "20001",
        "country": "United States",
        "isEligibleForExpressLane": false,
        "employerData": {
            "employer": "Switchboard",
            "occupation": "Engineer",
            "employerAddr1": null,
            "employerCity": null,
            "employerState": null,
            "employerCountry": null
        },
        "email": "shreyes@oneswitchboard.com",
        "phone": "8885551234"
    },
    "contribution": {
        "createdAt": "2023-06-09T15:59:27-04:00",
        "orderNumber": "AB1111",
        "contributionForm": "sticker103",
        "refcodes": {
            "refcode": "ref-Crane"
        },
        "refcode": "ref-Crane",
        "refcode2": null,
        "creditCardExpiration": null,
        "recurringPeriod": "once",
        "recurringDuration": 1,
        "weeklyRecurringSunset": null,
        "abTestName": null,
        "isRecurring": false,
        "isPaypal": true,
        "isMobile": false,
        "abTestVariation": null,
        "isExpress": false,
        "withExpressLane": false,
        "expressSignup": false,
        "uniqueIdentifier": "AqxHMqZAvjA",
        "textMessageOption": "opt_in",
        "giftDeclined": null,
        "giftIdentifier": null,
        "shippingName": null,
        "shippingAddr1": null,
        "shippingCity": null,
        "shippingState": null,
        "shippingZip": null,
        "shippingCountry": null,
        "smartBoostAmount": null,
        "customFields": [],
        "status": "approved",
        "thanksUrl": null
    },
    "lineitems": [
        {
            "sequence": 1,
            "entityId": 1,
            "fecId": "C00000",
            "committeeName": "Eric for Dogcatcher",
            "amount": "5.0",
            "paidAt": "2023-08-27T04:59:45-04:00",
            "paymentId": 242184335,
            "lineitemId": 600314606
        }
    ],
    "form": {
        "name": "sticker103",
        "kind": "page",
        "ownerEmail": null,
        "managingEntityName": "Eric for Dogcatcher",
        "managingEntityCommitteeName": "Eric for Dogcatcher"
    }
}
'
```

After sending the curl request, the lineitem appears successfully in the database table.
![alt text](image-2.png)

## Testing the API with the web browser
Visit `http://localhost:8000/recent_donations/entity/1` in your web browser to see data from the most recent 10 donations from the entity with `entity_id=1`

Visit `http://localhost:8000/aggregate_contributions/entity/1` to see the sum of all donations over all time for entity 1.

Visit `http://localhost:8000/aggregate_contributions/entity/1/days/1000` to see the sum of all donations over the past 1000 days.

### Analysis

I did spend about 6 hours on this project, but the first two or so were spent setting up a developer environment on this new laptop -- installing xcode, python, node, postgres, github, and re-orienting myself.

Lack of authentication for this API is a glaring issue I'd like to address next. I am new to FastAPI and chose to skip it for speed, but adding a token would be relatively simple.

There is minimal logging at the moment, but in the past I have used python's default logger and sent logs to datadog. I would love to add error logging to the `try/except` blocks and more sophisticated status logging. 

I was briefly using the pydantic library before removing it for simplicity, but I would like to add it back in to improve data validation, guarding against changes in the Actblue webhook json schema or in the sqlalchemy model. 

I wrote some unit tests to validate the sqlalchemy queries, but would like to add testing for the endpoints. I've used Github Actions for CI/CD in the past, and pytest integrates well with Github actions CI/CD.

I would choose to deploy the backend as a microservice, in a kubernetes container. 


