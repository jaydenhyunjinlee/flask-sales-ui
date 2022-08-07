from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import json
import os 

app = Flask(__name__)

# Connect the database for the web application
conf_fp = os.path.join(os.getcwd(), 'static', 'conf', 'conf.json')
with open(conf_fp, 'r') as f:
    conf = json.load(f)

db_name = conf['database']
username = conf['user']
pwd = conf['pwd']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{pwd}@localhost:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class sales(db.Model):
    # rowId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True)
    unitPrice = db.Column(db.Integer, default=0)
    status = db.Column(db.String(255))
    orderdate = db.Column(db.String(255))
    product_category = db.Column(db.String(255))
    sales_manager = db.Column(db.String(255))
    shipping_cost = db.Column(db.Integer)
    delivery_time = db.Column(db.Integer)
    shipping_address = db.Column(db.String(255))
    product_code = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<OrderID = {self.orderId}>'

# methods=['POST', 'GET'] for posting and getting data to the route
# and sending them to our database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # If data is input(Add data is clicked), consecutive page will show:
        task_orderid = request.form['orderid']
        # assert bool(task_orderid) & isinstance(task_orderid, int) & task_orderid < 1_000_000, 'Inappropriate value'
        
        task_quantity = request.form['quantity']
        # assert bool(task_quantity) & isinstance(task_quantity, int) & task_quantity < 500, 'Inappropriate value'

        task_unitprice = request.form['unitPrice']
        # assert bool(task_unitprice) & isinstance(task_unitprice, int) & task_unitprice < 1000, 'Inappropriate value'

        task_status = request.form['status']
        # assert bool(task_status) & isinstance(task_status, str), 'Inappropriate value'

        task_orderdate = request.form['orderdate']
        # assert bool(task_orderdate), 'Invalid orderdate'

        task_product_category = request.form['product_category']
        # assert bool(task_product_category) & isinstance(task_product_category, str), 'Invalid product category'

        task_sales_manager = request.form['sales_manager']
        task_shipping_cost = request.form['shipping_cost']
        task_delivery_time = request.form['delivery_time']
        task_shipping_address = request.form['shipping_address']
        task_product_code = request.form['product_code']
        new_sale = sales(
            orderId=task_orderid,
            quantity=task_quantity,
            unitPrice=task_unitprice,
            status=task_status,
            orderdate=task_orderdate,
            product_category=task_product_category,
            sales_manager=task_sales_manager,
            shipping_cost=task_shipping_cost,
            delivery_time=task_delivery_time,
            shipping_address=task_shipping_address,
            product_code=task_product_code)

        try:
            db.session.add(new_sale)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e) + '\n'
            return 'Task upload into db failed'
        
    else:
        tasks = sales.query.order_by(sales.last_updated).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:orderId>')
def delete(orderId):
    sale_to_delete = sales.query.get_or_404(orderId)

    try:
        db.session.delete(sale_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this'

@app.route('/update/<int:orderId>', methods=['POST', 'GET'])
def update(orderId):
    sale_to_update = sales.query.get_or_404(orderId)

    if request.method == 'POST':
        sale_to_update.orderId = request.form['orderId']
        sale_to_update.quantity = request.form['quantity']
        sale_to_update.unitPrice = request.form['unitPrice']
        sale_to_update.status = request.form['status']
        sale_to_update.orderdate = request.form['orderdate']
        sale_to_update.product_category = request.form['product_category']
        sale_to_update.sales_maanger = request.form['sales_manager']
        sale_to_update.shipping_cost = request.form['shipping_cost']
        sale_to_update.delivery_time = request.form['delivery_time']
        sale_to_update.shipping_address = request.form['shipping_address']
        sale_to_update.product_code = request.form['product_code']

        try:
            db.session.commit();
            return redirect('/')
        except:
            return 'There was a problem updating'
    else:
        return render_template('update.html', task=sale_to_update)
 
if __name__ == '__main__':
    app.run(debug=True)