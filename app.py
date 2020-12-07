from flask import Flask,jsonify,request
import sqlite3,json

app = Flask(__name__)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, authorization' )
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
  return response

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

######## Category #########
@app.route('/category',methods = ['GET'])
def category():
    try:
        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("select * from category")
        rows = cur.fetchall()
        cur.close()

        return jsonify(rows)
    except:
        jsonify({'status': 400,'message': 'Failed to read data from category table'}),400


@app.route('/category',methods = ['POST'])
def insertcategory():
    try:
        _json = request.json
        _category_name = _json['category_name']

        with sqlite3.connect("products.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO category(category_name) VALUES ('"+_category_name+"')")
            con.commit()
        cur.close()

        return jsonify({'status': 200,'message': 'Insert Successfull'}),200

    except:
        jsonify({'status': 400,'message': 'Failed to insert data into from product table'}),400

@app.route('/category',methods = ['PUT'])
def updatecategory():
    try:
        _json = request.json
        _id = _json['id']
        _category_name = _json['category_name']
        print(_id,_category_name)
        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("Update category set category_name = '"+_category_name+"' where id = "+_id)
        conn.commit()
        cur.close()

        return jsonify({'status': 201,'message': 'Update Successfull'}),201

    except:
        jsonify({'status': 400,'message': 'Failed to update from product table'}),400

@app.route('/category',methods = ['DELETE'])
def deletecategory():
    try:
        _json = request.json
        _id = _json['id']

        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE from category where id = "+_id)
        conn.commit()
        cur.close()

        return jsonify({'status': 202,'message': 'Delete Successfull'}),202

    except:
        jsonify({'status': 400,'message': 'Failed to delete record from product table'}),400


########## Product ###########
@app.route('/product',methods = ['GET'])
def product():
    try:
        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("select p.id,p.product_name,c.category_name from products p INNER JOIN category c ON p.category=c.id;")
        rows = cur.fetchall()
        cur.close()

        return jsonify(rows)

    except:
        jsonify({'status': 400,'message': 'Failed to read data from product table'}),400


@app.route('/product',methods = ['POST'])
def insertproduct():
    try:
        _json = request.json
        _product_name = _json['product_name']
        _category = _json['category']

        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("INSERT INTO products(product_name, category) VALUES ('"+_product_name+"',"+_category+")")
        conn.commit()
        cur.close()

        return jsonify({'status': 200,'message': 'Insert Successfull'}),200

    except:
        jsonify({'status': 400,'message': 'Failed to insert data into from product table'}),400

@app.route('/product',methods = ['PUT'])
def updateproduct():
    try:
        _json = request.json
        _id = _json['id']
        _product_name = _json['product_name']
        _category = _json['category']

        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("Update products set product_name = '"+_product_name+"', category = "+_category+" where id = "+_id)
        conn.commit()
        cur.close()

        return jsonify({'status': 201,'message': 'Update Successfull'}),201

    except:
        jsonify({'status': 400,'message': 'Failed to update from product table'}),400

@app.route('/product',methods = ['DELETE'])
def deleteproduct():
    try:
        _json = request.json
        _id = _json['id']

        conn = sqlite3.connect('products.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE from products where id = "+_id)
        conn.commit()
        cur.close()

        return jsonify({'status': 202,'message': 'Delete Successfull'}),202

    except:
        jsonify({'status': 400,'message': 'Failed to delete record from product table'}),400


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)