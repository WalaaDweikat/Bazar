from flask import Flask, json, jsonify ,render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
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
  #date_created = db.Column(db.DateTime, default=datetime.now)


  def __init__(self, book_id):
    self.book_id = book_id


class OrderSchema(ma.Schema):
  class Meta:
    fields = ('id', 'book_id')

# Init schema
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

###################################################################
# if client send purchase with a specific book_id
#order server send to catalog server
@app.route('/bazar/purchase/<int:book_id>', methods=['POST'])
def add_order(book_id):
  book_id = book_id
  #header
  #args = request.args
  #amount = args['amount']
  #body
  amount = request.form.get('amount')
  #here i want to send request to catalog server to ask about book qty
  r=requests.get("http://192.168.1.202:5000/bazar/available/"+str(book_id),{'amount':amount})
  temp=json.loads(r.content)
  print(temp['status'])
  #if response from the catalog => "available" post the order
  #else return error msg
  if temp['status']=="available":
    r2=requests.put("http://192.168.1.202:5000/bazar/decrease_quantity/"+str(book_id),{'amount':amount})
    temp2=r2.json()
    print(r2.json())
    new_order = Order(book_id)
    db.session.add(new_order)
    db.session.commit()
    #return order_schema.jsonify(new_order)
    return {"msg":f"bought book '{temp2.get('book_title')}'"}
  else: return(r.content)
###################################################################
#show the order list
@app.route('/show', methods=['GET'])
def show():
  orders=Order.query.all()
  result=orders_schema.dump(orders)
  return jsonify(result)

###################################################################
#home page
@app.route('/')
def home():
   return jsonify({'msg':'hello -order server'})

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
    return order_schema.jsonify(order)

###################################################################
#run
if __name__=="__main__":
    app.run(debug=True)
