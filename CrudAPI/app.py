"""This is a simple CRUD based REST API using Python, Flask and MongoDB, tested on Postman desktop application. 
TrailDB is my database name and movies is my collection name. Fields include "name","img" and "summary". """

#Importing all necessary packages
import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.errors import InvalidId
#import configapp
import logging
import configparser
import validators

#Access config.ini file for database
conf= configparser.ConfigParser()
conf.read(r'config.ini')
db= conf.get('paths', 'db_path')
# Another way is using a py file and importing it.


#Connect application to Database using Flask
app = Flask(__name__)
app.config["MONGO_URI"] =db 
#WITH .PY FILE:
#app.config["MONGO_URI"] =configapp.DBLINK
mongo=PyMongo(app)

#Indent the Jsonify output
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True #How to make this work? #Did not need

#Create a log file, with indentation
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def welcome():
    return jsonify("Welcome to CRUD API")


#Add validation for Create and Update
#Route to Add data
@app.route('/add', methods=['POST'])
def add_movie():
    _json = request.json
    _name = _json['name']
    _img= _json['img']
    _summary = _json['summary']
    if not validators.url(_img):
        return jsonify("Invalid URL in img field")
    try:
       if(type(_name)!= str or type(_summary)!= str):
           raise TypeError
    except(TypeError):
        return jsonify("Data Type for Name or Summary should be String")

    

    if _name and _img and _summary and request.method == 'POST':
        id = mongo.db.movies.insert_one({'name': _name, 'img': _img, 'summary': _summary})
        uidnum= json.loads(dumps(id.inserted_id))
        resp = jsonify("Movie data added successfully!", uidnum)
        resp.status_code = 200
        return resp
    else:
        return not_found()

#Route to read all data in the collection
@app.route('/read')
def movies():
    movies = mongo.db.movies.find()
    json_movies = json.loads(dumps(movies)) #Did this to prettyprint it
    resp = jsonify(json_movies)
    return  resp 

#Route to read data by the id passed
@app.route('/read/<id>')
def movie(id):
    try:
        check_id(id)
    except(InvalidId):
        return jsonify("Invalid ID")
    else:
        movie = mongo.db.movies.find_one({'_id': ObjectId(id)})
        json_movie=json.loads(dumps(movie))
        resp=jsonify(json_movie)
        return resp
    

#Route to update a particular data by id
@app.route('/update/<id>', methods=['PUT'])
def update_movie(id):
    try:
        check_id(id)
    except(InvalidId):
        return jsonify("Invalid ID")
    else:
        _id = id
        _json = request.json
        _name = _json['name']
        _img= _json['img']
        _summary = _json['summary']

        if not validators.url(_img):
            return jsonify("Invalid URL in img field")
        try:
            if(type(_name)!= str or type(_summary)!= str):
                raise TypeError
        except(TypeError):
            return jsonify("Data Type for Name or Summary should be String")
        #Question: How to update only 1 field
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
    try:
        check_id(id)
    except(InvalidId):
        return jsonify("Invalid ID")
    else:
        mongo.db.movies.delete_one({'_id': ObjectId(id)})
        resp= jsonify("Movie data deleted successfully! ID: ", id)
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

@app.errorhandler(400)
def wrongValue(error=None):
    message = {
        'status': 400,
        'message': 'Bad Value'
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

def check_id(id):
    readdata= mongo.db.movies.find_one({'_id': ObjectId(id)}) 
    if(readdata==None):
        return jsonify("No Such Uid")
    

#Run
if __name__ == "__main__":
    app.run(debug=True)

#Data Structures based Questions next round