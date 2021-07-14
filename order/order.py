from flask import Flask, jsonify ,render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import date
from datetime import datetime
import sqlite3
from flask_sqlalchemy.model import Model

#initial app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer)
  date_created = db.Column(db.DateTime, default=datetime.now)


  def __init__(self, book_id):
    self.book_id = book_id


class OrderSchema(ma.Schema):
  class Meta:
    fields = ('id', 'book_id','date_created')

# Init schema
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

###################################################################
# if client send purchase with a specific book_id
#order server send to catalog server
@app.route('/purchase/<int:book_id>', methods=['POST'])
def add_order(book_id):
  book_id = book_id
  #here i want to send request to catalog server to ask about book qty
  #if response from the catalog => "available" post the order
  #else return error msg
  new_order = Order(book_id)
  db.session.add(new_order)
  db.session.commit()
  return order_schema.jsonify(new_order)

###################################################################
##############test request
# @app.route('/purchase/<int:book_id>', methods=['GET'])
# def add_order(book_id):
#   book_id = book_id
#   catalog_url = 'http://10.0.2.15/query'
#   msg_data = {'book_id': book_id}
#   r = request.GET("http://10.0.2.15:5000/"+"query",{"book_id":book_id})

#   new_order = Order(book_id)
#   db.session.add(new_order)
#   db.session.commit()
#   return order_schema.jsonify(new_order)

###################################################################
#show the order list
@app.route('/show', methods=['GET'])
def show():
  orders=Order.query.all()
  return render_template('home.html',orders=orders)

###################################################################
#for catalog server
@app.route('/query/<int:book_id>', methods=['GET'])
def buy(book_id):
    args = request.args
    print (args) # For debugging
    qty_needed = args['qty']
    # no2 = args['key2']
    return jsonify(dict(data=[qty_needed])) # or whatever is required

###################################################################
#home page
@app.route('/')
def home():
   return jsonify({'msg':'hello ^-^'})

###################################################################
#home page
@app.route('/date')
def current_date():
  msg= date.today
  return {'msg':msg}

###################################################################
@app.route('/search/<int:order_id>')
def get_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    # return f'<h1>The book needed is: { order.book_id } </h1>'
    return render_template('order_info.html',book_id=order.book_id,time=order.date_created)

###################################################################
#run
if __name__=="__main__":
    app.run(debug=True)

###################################################################
# conn=sqlite3.connect('order.db')
# print("open")


# conn.close()

# courses = [
#     {
#     'name':"book_0",
#     "course_id" :"0",
#     'Description' : "book number 0",
#     'price' : "000"},
#     {
#     'name':"book_1",
#     'course_id' :"1",
#     'Description' : "book number 1",
#     'price' : "100"},
#     {
#     'name':"book_2",
#     'course_id' :"2",
#     'Description' : "book number 2",
#     'price' : "200"},
#     {
#     'name':"book_3",
#     'course_id' :"3",
#     'Description' : "book number 3",
#     'price' : "300"},
#      {
#     'name':"book_4",
#     'course_id' :"4",
#     'Description' : "book number 4",
#     'price' : "400"}
# ]




# @app.route("/courses",methods=['GET'])
# def get():
#     return jsonify({'courses':courses})


# @app.route("/courses/<int:course_id>",methods=['GET'])
# def get_course(course_id):
#     return jsonify({'course': courses[course_id]})


# @app.route("/courses",methods=['POST'])
# def create():
#     course={
#     'name':"book_5",
#     'course_id' :"5",
#     'Description' : "book number 5",
#     'price' : "500"}
#     courses.append(course)
#     return jsonify({'created': course})


# @app.route("/courses/<int:course_id>",methods=['PUT'])
# def course_update(course_id):
#     courses[course_id]['price']="100000"
#     return jsonify({'course': courses[course_id]})


# @app.route("/courses/<int:course_id>",methods=['DELETE'])
# def delete(course_id):
#     courses.remove(courses[course_id])
#     return jsonify({'result': True})



