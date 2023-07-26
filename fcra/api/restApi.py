from flask import Flask, Blueprint, jsonify, request, render_template
# from flask_restful import Resources
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
from flask_mysqldb import MySQL
import json
import mysql.connector
import requests
import face_recognition
import cv2
import os
import glob
import numpy as np
import base64
import io

restApi = Blueprint('restApi', __name__)

app = Flask(__name__)
# # app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "ROOT"
# app.config["MYSQL_DB"] = "student"

# mysql = MySQL(app)
mydb = mysql.connector.connect(
    host='localhost', user='root', password='ROOT', database='student')

# con=create_engine('mysql+pymysql://root:ROOT@localhost:3306/student')


@restApi.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        data = []
        cursor = mydb.cursor(buffered=True)
        query = "select * from student.l where Email=%s and Password=%s and Role=%s"
        obj = json.loads(request.data)
        value = [obj["Email"], obj["Password"], obj["Role"]]
        cursor.execute(query, value)
        all_data = cursor.fetchone()
        if all_data:
            data = {"Email": all_data[0],
                    "Password": all_data[1], "Role": all_data[2]}
            print(data)
            return json.dumps({"status": "successful", "Role": all_data[2]})
        else:
            return json.dumps({"status": "unsuccessful"})
    elif (request.method == 'POST'):
        cursor = mydb.cursor(buffered=True)
        query = "insert into student.l (Email,Password,Role) values (%s,%s,%s)"
        obj = json.loads(request.data)
        cursor.execute(query, (obj["Email"], obj["Password"], obj["Role"]))
        mydb.commit()
        return jsonify({"data": "Signup successful"})


@restApi.route('/api', methods=['GET', 'POST'])
def query_rec():
    if request.method == 'GET':
        cursor = mydb.cursor(buffered=True)
        query = "select * from student.s"
        cursor.execute(query)
        all_data = cursor.fetchall()

        data = []
        for i in all_data:
            data.append(({"id": i[0], "Image": i[1], "Name": i[2], "Email": i[3],
                          "Department": i[4], "Post": i[5], "Phone": i[6]}))
            # print("this is data", all_data[0], type(all_data[0]), '\n\n\n')
        # return jsonify({"data": all_data})
        # alldata = json.dumps(all_data)
        return json.dumps({"data": data})

    elif request.method == 'POST':
        cursor = mydb.cursor(buffered=True)
        query2 = "insert into student.s (Image,Name,Email,Department,Post,Phone) values (%s,%s,%s,%s,%s,%s)"
        obj = json.loads(request.data)
        print(obj)
        # obj = requests.get(url='127.0.0.1: 5000/')
        cursor.execute(
            query2, (obj["Image"], obj["Name"], obj["Email"], obj["Department"], obj["Post"], obj["Phone"]))
        mydb.commit()

        return json.dumps({"data": "data inserted"})


@restApi.route('/emp')
def emp():
    cursor = mydb.cursor()
    obj3 = json.loads(request.data)
    query5 = "select * from student.s where Email=%s"
    cursor.execute(query5, [obj3["Email"]])
    all_data = cursor.fetchone()
    query0 = "select anns from student.ann"
    cursor.execute(query0)
    annData = cursor.fetchall()
    annData0 = []
    for i in annData:
        annData0.append(i[0])
    dict1 = {"id": all_data[0], "Image": all_data[1], "Name": all_data[2], "Email": all_data[3],
             "Department": all_data[4], "Post": all_data[5], "Phone": all_data[6], "ann": annData0}
    mydb.commit()
    return json.dumps({"data": dict1})


@restApi.route('/apii', methods=['GET', 'POST', 'PUT'])
def query_rec2():
    print('hello')
    if request.method == 'POST':
        cursor = mydb.cursor(buffered=True)
        obj2 = json.loads(request.data)
        # obj is a dictionary here so we can access it by key value pair
        print(obj2, '\n\n\n')
        query3 = "update student.s set Name=%s,Email=%s,Department=%s,Post=%s,Phone=%s where id=%s"

        cursor.execute(query3, (obj2["Name"], obj2["Email"], obj2["Department"], obj2["Post"],
                                obj2["Phone"], obj2["id"]))  # we only want value here therefore we specified as obj["id"]

        mydb.commit()
        return json.dumps({"data": "data updated"})
    elif request.method == 'GET':
        cursor = mydb.cursor(buffered=True)
        obj = json.loads(request.data)
        print(obj, '\n\n\n')
        query4 = "delete from student.s where id=%s"
        cursor.execute(query4, [obj["id"]])
        mydb.commit()
        return json.dumps({"data": "data deleted"})


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path, name):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        # images_path = glob.glob(os.path.join(images_path, "."))

        # print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        # for img_path in images_path:

        img = images_path
        # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get the filename only from the initial file path.
        # basename = os.path.basename(images_path)
        # (filename, ext) = os.path.splitext(basename)
        # Get encoding
        im = face_recognition.load_image_file(img)
        img_encoding = face_recognition.face_encodings(im)[0]

        # Store file name and file encoding
        self.known_face_encodings.append(img_encoding)
        self.known_face_names.append(name)

        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            print("inside face")
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding)
            name = "Unknown"
            print('here', matches)
            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names


def convert_base64_to_frame(base64_data):
    # Decode the base64 data to raw bytes
    raw_data = base64.b64decode(base64_data)

    # Convert raw bytes to a NumPy array
    np_data = np.frombuffer(raw_data, dtype=np.uint8)

    # Convert NumPy array to an OpenCV image (frame)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    return frame


@restApi.route('/imageApi', methods=['GET', 'POST'])
def imageApiFun():
    print("Start Recognition \n\n\n")
    data = json.loads(request.data)
    cursor = mydb.cursor()

    query = "select Image,Name from  student.s where Email=%s"

    print('this is data', data.keys(), data["Email"])
    cursor.execute(query, [data["Email"]])
    imgBase64 = cursor.fetchone()
    img = base64.b64decode(imgBase64[0])
    img = io.BytesIO(img)
    image_np = np.frombuffer(img.read(), np.uint8)
    image_cv2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    cv2.imwrite('img.jpg', image_cv2)
    imageConv = convert_base64_to_frame(data["Image"])

    # Encode faces from a folder
    sfr = SimpleFacerec()
    print(imgBase64[1], '\n\n\n')
    sfr.load_encoding_images(img, imgBase64[1])
    face_locations, face_names = sfr.detect_known_faces(imageConv)

    print(face_names, '\n\n\n')
    return json.dumps({'result': face_names})

# @restApi.route('/image', methods=['GET', 'POST'])
# def image():
#     if request.method == 'POST':
#         cursor = mydb.cursor()

# my_data = student.s.query.get(obj["id"])

# app.secret_key = "Secret Key"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ROOT@localhost:3306/student'
# app.config['SQLALCHEMY_TRACK_MODIFICAIONS'] = True

# db = SQLAlchemy(app)

# class s(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100))
#     Email = db.Column(db.String(100))
#     Course = db.Column(db.String(100))
#     Phone = db.Column(db.String(100))
# db.create_all()

# def __init__(self, id, Name, Email, Course, Phone):
#     self.id = id
#     self.Name = Name
#     self.Email = Email
#     self.Course = Course
#     self.Phone = Phone
#     return (self.Name, self.Email, self.Course, self.Phone)

# @restApi.route('/api', methods=['GET', 'POST'])
# def query_rec():
#     if request.method == 'GET':
#         if db.session:
#             all_data = s.query.all()
#             data = []
#             for i in all_data:
#                 data.append({"id": i.id, "Name": i.Name, "Email": i.Email,
#                             "Course": i.Course, "Phone": i.Phone})
#             # print("this is data", all_data[0], type(all_data[0]), '\n\n\n')
#         # return jsonify({"data": all_data})
#         # alldata = json.dumps(all_data)
#         return jsonify({"data": data})

#     elif request.method == 'POST':

#         # Name = request.form['Name']
#         # Email = request.form['Email']
#         # Course = request.form['Course']
#         # Phone = request.form['Phone']
#         Name = request.form['Name']
#         Email = request.form['Email']
#         Course = request.form['Course']
#         Phone = request.form['Phone']
#         # print(Name, Email, Course, Phone)
#         with app.app_context():
#             my_data = s(Name, Email, Course, Phone)
#             db.session.add(my_data)
#             db.session.commit()
#         return jsonify({"data": "data inserted"})

# @restApi.route('/apii', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def query_rec2():
#     if request.method == 'POST':
#         obj = json.loads(request.data)

#         my_data = s.query.get(obj["id"])
#         my_data.Name = obj["Name"]
#         my_data.Email = obj["Email"]
#         my_data.Course = obj["Course"]
#         my_data.Phone = obj["Phone"]
#         print('second print', my_data.Name, my_data.Email,
#               my_data.Course, my_data.Phone)
#         with app.app_context():
#             db.session.commit()
#         return jsonify({"msg": "you are in post-update"+str(obj['id'])})
#     elif request.method == 'PUT':
#         return jsonify({"msg": "you are in put"})
#     elif request.method == 'DELETE':
#         return jsonify({"msg": "you are in delete"})
# elif request.method == 'PATCH':
#     return jsonify({"msg": "you are in patch"})
# elif request.method == 'HEAD':
#     return jsonify({"msg": "you are in head"})
# elif request.method == 'OPTIONS':


@restApi.route('/todo-task', methods=['GET', 'POST'])
def todoFun():
    if request.method == "GET":
        cursor = mydb.cursor()
        email = json.loads(request.data)
        print(email)
        query = "select task from student.todo where Email=%s and flag='True'"
        cursor.execute(query, [email['email']])
        all_data = cursor.fetchall()
        return json.dumps({"data": all_data})

    elif request.method == "POST":
        cursor = mydb.cursor()
        print('hello')
        query = "insert into student.todo (task,Email) values (%s,%s)"
        data = json.loads(request.data)
        email = data["Email"]
        task = data["task"][0]
        cursor.execute(query, [task, email])
        mydb.commit()

        query = "select task from student.todo where Email=%s and flag=%s"
        cursor.execute(query, [email, 'True'])
        all_data = cursor.fetchall()

        data = []
        for i in all_data:
            data.append({"task": i[0]})
            # print("this is data", all_data[0], type(all_data[0]), '\n\n\n')
        # return jsonify({"data": all_data})
        # alldata = json.dumps(all_data)
        return json.dumps({"data": data})


@restApi.route('/deletetask', methods=['POST'])
def deletetaskFun():
    if request.method == "POST":
        data = json.loads(request.data)
        print('you are in post')
        con = mydb.cursor()
        query = "update student.todo set flag=%s where Email=%s and task=%s"
        val = ['False', data['Email'], data['task']]
        con.execute(query, val)
        mydb.commit()
        return json.dumps({"data": "Done"})


@restApi.route('/announcements', methods=['GET', 'POST'])
def announcementsFun():
    if request.method == "POST":
        data = json.loads(request.data)
        con = mydb.cursor(buffered=True)
        query = "insert into student.ann(anns) values (%s)"
        annou = data['announcement']
        con.execute(query, [annou])
        mydb.commit()
        return jsonify({"data": "you are in post"})
