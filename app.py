from flask import render_template, request, jsonify
from models import *
from marshmallow import ValidationError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# API routes

@app.route("/api/products", methods=['GET', 'POST'])
def view_products_api():
    # GET
    if request.method == 'GET':
        products = Products.query.all()
        products_displayed = products
        # pagination option: specify page (page number) and per_page(number of products per page)
        page = request.args.get('page')
        per_page = request.args.get('per_page')
        if page:
            total = len(products)
            if not per_page:
                per_page = total
            print((int(page)-1)*int(per_page)+int(per_page))
            if (int(page)-1)*int(per_page) >= total:
                return jsonify({"error": "No enough products to display"}), 404
            products_displayed = products[(int(page)-1)*int(per_page):(int(page)-1)*int(per_page)+int(per_page)]
        products_json = ProductsSchema(many=True).dump(products_displayed).data
        return jsonify(products_json)

    # POST
    if request.method == 'POST':
        req = request.get_json()
        product = ProductsSchema().load(req).data
        db.session.add(product)
        db.session.commit()
        return jsonify({'Added product': product.description}), 201

@app.route("/api/products/<int:product_id>", methods=['GET', 'PUT', 'DELETE'])
def view_product_api(product_id):
    product = Products.query.get(product_id)
    if product is None:
        return jsonify({"error": "Invalid product_id"}), 404

    # GET
    if request.method == 'GET':
        product_json = ProductsSchema().dump(product).data
        return jsonify(product_json)

    # PUT
    if request.method == 'PUT':
        description = request.json['description']
        product.description = description
        db.session.commit()
        return jsonify({'Updated product description': product.description})

    # DELETE
    if request.method == 'DELETE':
        description = product.description
        db.session.delete(product)
        db.session.commit()
        return jsonify({'Deleted product': description})

@app.route("/api/products/<int:product_id>/locations", methods=['GET', 'POST'])
def view_locations_api(product_id):
    product = Products.query.get(product_id)
    if product is None:
        return jsonify({"error": "Invalid product_id"}), 404

    # GET
    if request.method == 'GET':
        locations = Locations.query.filter_by(product_id=product_id).all()
        locations_displayed = locations
        # pagination option: specify page (page number) and per_page(number of products per page)
        page = request.args.get('page')
        per_page = request.args.get('per_page')
        if page:
            total = len(locations)
            if not per_page:
                per_page = total
            print((int(page)-1)*int(per_page)+int(per_page))
            if (int(page)-1)*int(per_page) >= total:
                return jsonify({"error": "No enough locations to display"}), 404
            locations_displayed = locations[(int(page)-1)*int(per_page):(int(page)-1)*int(per_page)+int(per_page)]
        locations_json = LocationsSchema(many=True).dump(locations_displayed).data
        return jsonify(locations_json)

    # POST
    if request.method == 'POST':
        req = request.get_json()
        try:
            location = LocationsSchema().load(req).data
        except ValidationError:
            return jsonify({'Please verify location data for ': product_id}), 404
        location.product_id = product_id
        db.session.add(location)
        db.session.commit()
        return jsonify({'Added location for product ': product_id}), 201

@app.route("/api/products/<int:product_id>/locations/<int:location_id>", methods=['GET', 'PUT', 'DELETE'])
def view_location_api(product_id, location_id):
    product = Products.query.get(product_id)
    if product is None:
        return jsonify({"error": "Invalid product_id"}), 404
    location = Locations.query.filter_by(product_id=product_id,id =location_id).first()
    if location is None:
        return jsonify({"error": "Invalid location_id for this product"}), 404

    # GET
    if request.method == 'GET':
        location_json = LocationsSchema().dump(location).data
        return jsonify(location_json)

    # PUT
    if request.method == 'PUT':
        datetime = request.json['datetime']
        longitute = request.json['longitute']
        latitude = request.json['latitude']
        elevation = request.json['elevation']
        location.datetime = datetime
        location.longitute = longitute
        location.latitude = latitude
        location.elevation = elevation
        db.session.commit()
        return jsonify({'Updated location': location_id})

    # DELETE
    if request.method == 'DELETE':
        db.session.delete(location)
        db.session.commit()
        return jsonify({'Deleted location': location_id})

# simple GUI for adding current location

@app.route('/')
def index():
    products = Products.query.all()
    return render_template("index.html", list=products)

@app.route("/add_location", methods=['POST'])
def add_location():
    product_id = int(request.form.get("product_id"))
    product = Products.query.get(product_id)
    try:
        product.add_location(request.form.get("longitute"), request.form.get("latitude"), request.form.get("elevation"))
    except ValueError:
        return render_template("error.html", message="Invalid input format")
    return render_template("confirmation.html", description=product.description)

@app.route("/product<int:product_id>", methods=['GET', 'POST'])
def view_product(product_id):
    product = Products.query.get(product_id)
    if product is None:
        return render_template("error.html", message="No product with this id.")

    locations = product.locations
    return render_template("product.html", product=product, locations=locations)

if __name__ == '__main__':
    app.run()