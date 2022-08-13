from crypt import methods
from flask import Flask, jsonify
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from mongoengine import SequenceField
import bson.json_util as json_util
import json

client = MongoClient('localhost:27017')
db = client.EmployeeDB

app = Flask(__name__)

designation = ["manager","engineer","architect"]
marriage_status = ["yes","no"]

@app.route("/add_employee", methods = ['POST'])
def add_employee():
    try:
        data = json.loads(request.data)
        employee_id = data['id']
        employee_name = data['name']
        employee_age = data['age']
        employee_salary = data['salary']
        employee_experience = data['experience']
        employee_designation = data['designation']
        employee_married = data['married']
        employee_country = data['country']

        employee_designation = employee_designation.lower()
        employee_married = employee_married.lower()
        if employee_designation not in designation:
            return dumps({'message' : 'Designation should be manager, engineer or architect'})
        elif employee_married not in marriage_status:
            return dumps({'message' : 'Marraiage status should be yes or no'})
        elif employee_designation == "architect" and employee_experience < 5:
            return dumps({'message' : 'Architetc should have atleast 5 years of experience'})


        status = db.employees.insert_one({
            "id": employee_id,
            "name":employee_name,
            "age": employee_age,
            "salary":employee_salary,
            "designation": employee_designation,
            "experience": employee_experience,
            "married": employee_married,
            "country": employee_country
        })
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/employees", methods = ['GET'])
def get_all_employees():
    try:
        employees = list(db.employees.find())
       
        return app.response_class(json_util.dumps(employees), mimetype="application/json")

    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employee/<id>', methods = ['GET'])
def get_employee(id):
    try:
        id = int(id)
        employees = db.employees.find_one({'id': id})
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    
    try:
        id = int(id)
        data = json.loads(request.data)
        employee_name = data['name']
        employee_age = data['age']
        employee_salary = data['salary']
        employee_experience = data['experience']
        employee_designation = data['designation']
        employee_married = data['married']	
        employee_country = data['country']
        db.employees.update_one(
                {"id": id},
                {
                    "$set": {
                        "name":employee_name,
                        "age":employee_age,
                        "country":employee_country,
                        "salary":employee_salary,
                        "designation": employee_designation,
                        "experience": employee_experience,
                        "married": employee_married
                    }
                }
            )
        return app.response_class(json_util.dumps("SuccessFully Updated"), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    try:
        id = int(id)
        db.employees.delete_many({"id":id})
        return app.response_class(json_util.dumps("SuccessFully Deleted"), mimetype="application/json")

    except Exception as e:
        return dumps({'error' : str(e)})
    
@app.route('/employees/married/salary', methods = ['GET'])
def get_all_designation_married_salary():
    try:
        employees = db.employees.find({
            "$and": [
            { "salary": {"$gte": 8000}},
            { "married": "yes"}
        ]
        },
        {
            "designation":1
        })
        employees = list(employees)
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

    
@app.route('/employees/managers', methods = ['GET'])
def get_all_managers_morethan_fifteenyears():
    try:
        employees = db.employees.find({
            "$and": [
            { "experience": {"$gte": 15}},
            { "designation": "manager"}
        ]
        })
        employees = list(employees)
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employees/engineers/salary', methods = ['GET'])
def get_all_engineers_salary_lessthan_fivethousand():
    try:
        employees = db.employees.find({
            "$and": [
            { "salary": {"$lt": 5000}},
            { "designation": "engineer"}
        ]
        })
        employees = list(employees)
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employees/architect/age', methods = ['GET'])
def get_all_architects_age_morethan_forty():
    try:
        employees = db.employees.find({
            "$and": [
            { "age": {"$gt": 40}},
            { "designation": "architect"}
        ]
        })
        employees = list(employees)
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/employees/experience', methods = ['GET'])
def get_all_designation_experience_lessthan_five():
    try:
        employees = db.employees.find({
            "experience": {"$lt": 5}
        },
        {
            "designation":1
        })
        employees = list(employees)
        return app.response_class(json_util.dumps(employees), mimetype="application/json")
    except Exception as e:
        return dumps({'error' : str(e)})

if __name__ == "__main__":
    app.run(debug=True)