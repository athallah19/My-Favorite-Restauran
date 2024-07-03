from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi

app = Flask(__name__)

password = 'sparta'
cxn_str = f'mongodb+srv://test:{password}@cluster0.5qv8bta.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta2

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/restaurants', methods=["GET"])
def get_restaurants():
    restaurants = list(db.restaurants.find({}, {'_id': False}))
    return jsonify({
        'result': 'success',
        'restaurants': restaurants,
})

@app.route('/map')
def map_example():
    return render_template('prac_map.html')

@app.route("/restaurant/create", methods=["POST"])
def create_restaurant():
    name = request.form.get('name')
    categories = request.form.get('categories')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    doc = {
        'name': name,
        'categories': categories,
        'location': location,
        'coordinates': [longitude, latitude],
    }
    db.restaurants.insert_one(doc)
    return jsonify({
        "result": "success",
        "msg": "You successfully created a restaurant!"
    })

@app.route("/restaurant/delete", methods=["POST"])
def delete_restaurant():
    name = request.form.get('name')
    db.restaurants.delete_one({'name': name})
    return jsonify({
        "result": "success",
        "msg": "You successfully deleted a restaurant!"
    })

@app.route('/prac')
def prac_example():
    return render_template('map.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)