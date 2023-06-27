from flask import Flask, render_template, request , redirect, url_for, flash,json
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ROOT@localhost:3306/student'
app.config['SQLALCHEMY_TRACK_MODIFICAIONS'] = True

db = SQLAlchemy(app)

class s(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Course = db.Column(db.String(100))
    Phone = db.Column(db.String(100))

    def __init__(self, Name, Email, Course, Phone):
        self.Name= Name
        self.Email = Email
        self.Course = Course
        self.Phone = Phone
    



@app.route('/')
def testdb():
    res=requests.get(url='http://127.0.0.1:5001/api')
    data=res.json()
    print(data['data'])
    # try:
    #  with app.app_context():
    #     if db.session:
    #         all_data = s.query.all()
    #         return render_template("index.html", students = all_data )
    # except:
    #     return '<h1>Something is broken.</h1>'
    
    
    


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        id 
        Name = request.form['Name']
        Email = request.form['Email']
        Course = request.form['Course']
        Phone = request.form['Phone']
        with app.app_context():
            my_data = s(Name, Email, Course, Phone)
            db.session.add(my_data)
            db.session.commit()
            
        flash("Student Inserted Successfully!")
        return redirect(url_for('testdb'))

    return render_template('index.html')

@app.route('/update', methods= ['POST']) 
def update():

    if request.method == 'POST':
        
        my_data = s.query.get(request.form.get('id'))

        my_data.Name = request.form['Name']
        my_data.Email = request.form['Email']
        my_data.Course = request.form['Course']
        my_data.Phone = request.form['Phone']
        db.session.commit()
        print(my_data.Name)
        flash('Student Data Updated Successfully')

        return redirect(url_for('testdb'))
    
@app.route('/delete/<int:id>', methods = ['POST','GET'])
def delete(id):
        print(id)

        sc=s.query.filter_by(id=id).first()
        if sc:
            db.session.delete(sc)
            db.session.commit()
        flash('Student deleted successfully!')
        return redirect(url_for('testdb'))




if __name__ == "__main__":
    app.run(debug=True)
