from flask import Flask, json, jsonify ,render_template
from flask import request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


#front end tier will send requests to order server and catalog server 


#initial app
app = Flask(__name__)

#request to get all of the books information # it is sent to the catalog server
@app.route('/bazar/info/all', methods=['GET'])
def info():
  r = requests.get("http://192.168.1.202:5000/bazar/info/all")
  return (r.content)

#request to catalog to get info about book with the id book_id
@app.route('/bazar/info/<int:book_id>', methods=['GET'])
def get_info(book_id):
  book_id = book_id
  #this is the request to be sent to the catalog server
  r = requests.get("http://192.168.1.202:5000/bazar/info/"+str(book_id))
  return (r.content)

#getting the books info which have the topic s_topic #request to catalogServer
@app.route('/bazar/search/<s_topic>', methods=['GET'])
def search(s_topic):
  s_topic = s_topic
  #this is the request to be sent to the catalogServer
  r = requests.get("http://192.168.1.202:5000/bazar/search/"+str(s_topic))
  return (r.content)

#purchase to order server, there is a parameter called amount can be send with the request body to 
#specify how many books to purchase it will 1 by default if there is no body sent with the request 
@app.route('/bazar/purchase/<int:book_id>', methods=['POST'])
def purchase(book_id):
  book_id = book_id
  # args=request.args
  # amount=args['amount']
  #amount=request.json['amount']
  if request.data:#if there is an amount sent with the request`s body 
     amount=request.json['amount']
  else :
     amount=1 #the default value is one 
  #this is the reqest to be sent to the order server
  r = requests.post("http://192.168.1.203:5000/bazar/purchase/"+str(book_id),data={'amount':amount}) 
  return (r.content)

############################################################# for admin ######################################
#the following requests is sent form the admin of the book store 

#update the price of a book 
@app.route('/bazar/update_price/<int:book_id>', methods=['PUT'])
def update_book_price(book_id):
  book_id = book_id
  price = request.json['price']
  # args=request.args
  # price=args['price']
  r = requests.put("http://192.168.1.202:5000/bazar/update_price/"+str(book_id),data={'price':price})
  return (r.content)


#increase quantity 
@app.route('/bazar/increase_quantity/<int:book_id>', methods=['PUT'])
def increase_book_quantity(book_id):
  book_id = book_id
  amount = request.json['amount']
  # args=request.args
  # price=args['price']
  r = requests.put("http://192.168.1.202:5000/bazar/increase_quantity/"+str(book_id),data={'amount':amount})
  return (r.content)

#decrease quantity 
@app.route('/bazar/decrease_quantity/<int:book_id>', methods=['PUT'])
def decrease_book_quantity(book_id):
  book_id = book_id
  amount = request.json['amount']
  # args=request.args
  # price=args['price']
  r = requests.put("http://192.168.1.202:5000/bazar/decrease_quantity/"+str(book_id),data={'amount':amount})
  return (r.content)

#to show the orders list
@app.route('/bazar/order/show', methods=['GET'])
def show():
  r = requests.get("http://192.168.1.203:5000/show")
  return (r.content)
#catalog= 202
#order = 203
#run
if __name__=="__main__":
    app.run(debug=True)