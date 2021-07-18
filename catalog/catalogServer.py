from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.fields import Integer

#init app
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogDB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init database
db = SQLAlchemy(app)

#init marshmallow
ma = Marshmallow(app)

#catalog Class/Model
class Catalog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    topic = db.Column(db.String(200))
     

    def __init__(self,id,title,quantity,price,topic):
        self.id=id
        self.title=title
        self.quantity=quantity
        self.price=price
        self.topic=topic


#Catalog schema
class CatalogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title' , 'quantity' , 'price' , 'topic')

#init schema
book_schema = CatalogSchema()
books_schema = CatalogSchema(many=True)


#return the all books information in the database
@app.route("/bazar/info/all", methods=['GET'])
def get_books():
    all_books = Catalog.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)


#return the information about the book with the id s_id
@app.route("/bazar/info/<s_id>", methods=['GET'])
def get_book_id(s_id):
    book = Catalog.query.with_entities(Catalog.title,Catalog.quantity,Catalog.topic,Catalog.price).filter_by(id = s_id).first()
    return book_schema.jsonify(book)


#return the information about the book with the topic s_topic
@app.route("/bazar/search/<s_topic>", methods=['GET'])
def get_book_topic(s_topic):
    books = Catalog.query.with_entities(Catalog.id,Catalog.title).filter_by(topic=s_topic.replace("%20"," ")).all()
    result =jsonify(books_schema.dump(books))
    return result


#This endpoint is used by the order server to check if there is enough amount of purchased books
#when the client uses the endpoint '/bazar/purchase/<int:book_id>' (this endpoint in the order server) the order server will send a query to the catalog 
#to now the if the quantity of the books in the store is sufficient 
#if sufficient, the order will send an update query to the catalog to decrease the quantity of books by the amount
@app.route("/bazar/available/<book_id>",methods=['GET'])
def search(book_id):
    book = Catalog.query.get(book_id)
    if book:
        args = request.args
        amount = int(args['amount'])
        #there is no enough books to purchase
        if book.quantity - amount < 0:
            return jsonify({"status":"not enough","the remaining quantity of books is less than the ordered books which are " : book.quantity })
        else :
            #the book quantity is enough to purchase
            return jsonify({"status":"available"})
    else:  return jsonify({"status":"not found",book_id : "this id does not exist"})


#This is for decreasing the quantity of books in the database by the amount which is sent with the request body 
#This end point is used by the order server (Update) for the purchase request
@app.route("/bazar/decrease_quantity/<book_id>",methods=['PUT'])
def decrease_book_quantity(book_id):
    book = Catalog.query.get(book_id)
    if book:
        amount = int(request.form.get('amount'))
        if book.quantity - amount < 0:
            return jsonify({"msg":f"not enough ,the remaining quantity of books is less than the required books which are {book.quantity}"})
        elif book.quantity - amount == 0 :
            book.quantity = 0  
            db.session.commit()
            return jsonify({"book_title":book.title,"msg" : f"decrease of '{book.title}' book quantity ,the quantity now is {book.quantity}"})
        else :
            book.quantity = book.quantity - amount 
            db.session.commit()
            return jsonify({"book_title":book.title,"msg" : f"decrease of '{book.title}' book quantity ,the quantity now is {book.quantity}"})
    else:  return jsonify({book_id : "this id does not exist"})


#increasing the book quantity by the amount 
#this endpoint to be used by the bookstore admin 
@app.route("/bazar/increase_quantity/<book_id>",methods=['PUT'])
def increase_book_quantity(book_id):
    book = Catalog.query.get(book_id)
    if book:
        #amount = request.json['amount']
        #args = request.args
        #amount = int(args['amount'])
        amount = int(request.form.get('amount'))
        book.quantity = book.quantity + amount 
        db.session.commit()
        return jsonify({"msg" : f"increase of '{book.title}' book quantity,the quantity now is {book.quantity}"})
    else:  return jsonify({book_id : "this id does not exist"})


#updating the book price 
#this also to be used by the admin
@app.route("/bazar/update_price/<book_id>",methods=['PUT'])
def update_book_price(book_id):
    book = Catalog.query.get(book_id)
    if book:
        #price = request.json['price']
        #args = request.args
        #price = int(args['price'])
        price = request.form.get('price')
        book.price = price 
        db.session.commit()
        return book_schema.jsonify(book)
    else:  return jsonify({book_id : "this id does not exist"})


@app.route("/",methods=['GET'])
def home():
    return jsonify({'msg':'home'})

if __name__ == '___main__':
    app.run(debug=True)