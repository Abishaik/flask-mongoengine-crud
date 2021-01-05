#Required Modules
from flask import Flask,jsonify,request
from mongoengine import connect,Document, StringField,IntField
from mongoengine.errors import NotUniqueError
import json

#Class:
class Student(Document):
    name = StringField(max_length=50)
    age=IntField()

#To connect to MongoDB
connect(
    db="home",
    host="localhost",
    port=27017)

#Instance for App
app = Flask(__name__)

#Flask----->
@app.route("/start",methods=["GET"])
def start():

    return "Going to see CRUD operations using mongoengine"


#CRUD(Create, Read, Update and Delete) Operations in Functions inside Routes:

#1.Create Operation:
@app.route("/add",methods=["POST"])
def add():
    try:
        #Here we create student with Defined name and age in Program
        studentval= Student( name="Ajith")
        studentval.age=10
        studentval.save()
        #Query
        student_db = Student.objects().as_pymongo().to_json()

        return "Student data created"
    except NotUniqueError as e:
        print("Unique Error")

@app.route("/create",methods=["POST"])
def create():
    #Here we create student using data from User input in JSON format
    stud_json=request.get_json()
    try:
        #Taking Variables from JSON
        studentval= Student( name=stud_json["name"])
        studentval.age=stud_json["age"]
        studentval.save()
        #Query
        student_db = Student.objects().as_pymongo().to_json()
        
        return "Student data added"
    except NotUniqueError as e:
        return "Unique Error"
    #Sample Input in Postman body:
    # {
    # "name":"Abishaik S",
    # "age":21
    # }

#2.Read Operation:       
@app.route("/show" ,methods=["GET"])
def show():
    #Query for all students
    studentval = Student.objects().as_pymongo().to_json()

    return studentval ,200

@app.route("/show/<string:name1>" ,methods=["GET"])
def show_by_name(name1):
    #Query for particular student
    studentval = Student.objects(name=name1).as_pymongo().to_json()

    return studentval ,200

#3.Update Operation:(Here we also use "PUT" or "PATCH" methods)
@app.route("/update/<string:name1>" ,methods=["POST"])
#sample path = /update/Abishaik 
def update_student(name1):
    #got name in param
    stud_json=request.get_json()
    #Query
    suudentval2 = Student.objects(name=name1)
    suudentval2.update(**stud_json)
    student_db = Student.objects().as_pymongo().to_json()
    
    return student_db ,200
    #Sample Input in Postman body:
    # {
    # "name":"Abishaik",
    # "age":27
    # }

#4.Delete Operation:
@app.route("/delete/<string:name1>" ,methods=["POST"])
def delete_student(name1):
    #Query
    suudentval2 = Student.objects(name=name1).delete()
    student_db = Student.objects().as_pymongo().to_json() 
     
    return student_db ,200

#app to run standalone
if __name__=="__main__":
   app.run(debug=True)





#Fully working---------------------------------------------------------------------------