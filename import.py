import os
import csv
from flask import Flask, render_template, request
from models import *
from datetime import datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # create a new DB
    from app import db
    db.drop_all()
    db.create_all()

    # import data from given file
    f = open("records.csv")
    reader = csv.reader(f)
    for id, description, datetime_str, longitute, latitude, elevation in reader:
        # import to Products table
        if db.session.query(Products.id).filter_by(id=id).scalar() is None:
            product = Products(id=id, description=description)
            db.session.add(product)
            print(f"Added product id: {id}, description: {description}.")

        # import to Locations table
        formatted_datetime = datetime.strptime(datetime_str[:-3]+datetime_str[-2:], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)
        location = Locations(datetime=formatted_datetime, longitute=longitute, latitude=latitude, elevation=elevation, product_id=id)
        db.session.add(location)
        print(f"Added location datetime: " + formatted_datetime.strftime("%Y-%m-%dT%H:%M:%S%z") + f", longitute: {longitute}, latitude: {latitude}, elevation: {elevation}, product_id: {id}.")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()