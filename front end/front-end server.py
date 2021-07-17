from flask import Flask, json, jsonify ,render_template
from flask import request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#initial app
app = Flask(__name__)

@app.route('/bazar/info/all', methods=['GET'])
def info():
  r = requests.get("http://192.168.1.202:5000/bazar/info/all")
  return (r.content)


@app.route('/bazar/info/<int:book_id>', methods=['GET'])
def get_info(book_id):
  book_id = book_id
  r = requests.get("http://192.168.1.202:5000/bazar/info/"+str(book_id))
  return (r.content)


@app.route('/bazar/search/<s_topic>', methods=['GET'])
def search(s_topic):
  s_topic = s_topic
  r = requests.get("http://192.168.1.202:5000/bazar/search/"+str(s_topic))
  return (r.content)


@app.route('/bazar/purchase/<int:book_id>', methods=['GET'])
def purchase(book_id):
  book_id = book_id
  args=request.args
  amount=args['amount']
  r = requests.get("http://192.168.1.203:5000/bazar/purchase/"+str(book_id),{'amount':amount})
  return (r.content)

#run
if __name__=="__main__":
    app.run(debug=True)