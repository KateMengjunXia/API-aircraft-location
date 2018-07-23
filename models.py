from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validates_schema, post_load, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    locations = db.relationship("Locations", backref="product", lazy=True, cascade='delete')

    def add_location(self, longitute, latitude, elevation):
        longitute_float = float(longitute)
        latitude_float = float(latitude)
        elevation_int = int(elevation)
        if longitute_float < -180 or longitute_float > 180 or latitude_float < -90 or latitude_float > 90:
            raise ValueError
        location = Locations(datetime=datetime.utcnow(), longitute=longitute_float, latitude=latitude_float, elevation=elevation_int, product_id=self.id)
        db.session.add(location)
        db.session.commit()

class Locations(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    longitute = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

# model schema for products
class ProductsSchema(ma.ModelSchema):
    class Meta:
        model = Products

# schema to validate serialize, and deserialize data for location
class LocationsSchema(Schema):
    __model__ = Locations

    datetime = fields.DateTime()
    longitute = fields.Float(required=True)
    latitude = fields.Float(required=True)
    elevation = fields.Integer(required=True)

    @post_load
    def make_location(self, data):
        return self.__model__(**data)

    @validates_schema
    def validate_input(self, data):
        if float(data['longitute']) < -180 or float(data['longitute']) > 180:
            raise ValidationError('Longitute must be between -180 and 180')
        if float(data['latitude']) < -90 or float(data['latitude']) > 90:
            raise ValidationError('Latitude must be between -90 and 90')
