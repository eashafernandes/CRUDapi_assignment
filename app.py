"""This is a simple CRUD based REST API using Python, Flask and MongoDB, tested on Postman desktop application. 
TrailDB is my database name and movies is my collection name. Fields include "name","img" and "summary". """

#Importing all necessary packages
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

#Connect application to Database using Flask
app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb://localhost:27017/TrailDB"
mongo=PyMongo(app)

#Route to Add data
@app.route('/add', methods=['POST'])
def add_movie():
    _json = request.json
    _name = _json['name']
    _img= _json['img']
    _summary = _json['summary']

    if _name and _img and _summary and request.method == 'POST':
        id = mongo.db.movies.insert_one({'name': _name, 'img': _img, 'summary': _summary})
        resp = jsonify("Movie data added successfully!")
        resp.status_code = 200
        return resp
    else:
        return not_found()

#Route to read all data in the collection
@app.route('/read')
def movies():
    movies = mongo.db.movies.find()
    resp = dumps(movies)
    return resp 

#Route to read data by the id passed
@app.route('/read/<id>')
def movie(id):
    movie = mongo.db.movies.find_one({'_id': ObjectId(id)})
    resp=dumps(movie)
    return resp

#Route to update a particular data by id
@app.route('/update/<id>', methods=['PUT'])
def update_movie(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _img= _json['img']
    _summary = _json['summary']

    if _name and _img and _summary and request.method == 'PUT':
        mongo.db.movies.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            { '$set': {'name': _name, 'img':_img, 'summary': _summary}}
        )

        resp = jsonify("Movie data updated successfully!")
        resp.status_code = 200
        return resp
    else:
        return not_found()


#Route to delete a particular data by id
@app.route('/delete/<id>', methods = ['DELETE'])
def delete_user(id):
    mongo.db.movies.delete_one({'_id': ObjectId(id)})
    resp= jsonify("Movie data deleted successfully!")
    resp.status_code = 200
    return resp


#Error Handling
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found'
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

#Run
if __name__ == "__main__":
    app.run(debug=True)

