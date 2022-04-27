from crypt import methods
from click import BadParameter
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import datetime
from datetime import timezone
import hashlib


app = Flask(__name__)
dt = datetime.datetime.utcnow()


# try:
#conn = psycopg2.connect("dbname='myduka' user='postgres' host='localhost' password='1234'")
conn = psycopg2.connect("dbname='dcq2mm2ag4dcdn' user='qhdfbpkgxbngyh' host='ec2-52-48-159-67.eu-west-1.compute.amazonaws.com' password='c37598ff2e5d8d06eebaa1158209d9de42b60038e46cb1d52c11874f20a6b39a'")

# except:
#     print ("I am unable to connect to the database")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY, name VARCHAR (100) NOT NULL, buying_price VARCHAR (30)  NOT NULL, selling_price VARCHAR (30) NOT NULL, stock_quantity VARCHAR (30) NOT NULL);""")
cur.execute("""CREATE TABLE IF NOT EXISTS sales (id serial PRIMARY KEY,pid integer REFERENCES products(id), quantity VARCHAR (30) NOT NULL, created_at VARCHAR (30) NOT NULL);""")
conn.commit()



@app.route('/')
def home():
    return render_template("index.html")

# Route for handling the login page logic

@app.route('/save-inventory', methods=['post'])
def save_product():
    n = request.form["name"]
    bp = request.form["buying_price"]
    sp = request.form["selling_price"]
    sq = request.form["stock_quantity"]
    cur = conn.cursor()
    postgres_insert_query = """INSERT into products(name, buying_price, selling_price, stock_quantity) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (n,bp,sp,sq)
    cur.execute(postgres_insert_query, record_to_insert)
    return redirect ('inventory')
    


#property for capturing input name attr as dictionary keys :request.form


@app.route('/make-sale', methods=['post'])
def make_sale():
    n = request.form["quantity"]
    bp=request.form["pid"]
    cur = conn.cursor()
    postgres_insert_query = """INSERT into sales(pid, quantity,created_at) VALUES (%s,%s,%s)"""
    record_to_insert = (bp,n,dt)
    cur.execute(postgres_insert_query, record_to_insert)
    return redirect ('sales')



@app.route("/sales")
def sales():
    cur = conn.cursor()
    cur.execute("""SELECT * from sales""")
    rows = cur.fetchall()
    cur = conn.cursor()
    # cur.execute("""SELECT name from products""")
    # name = cur.fetchall()
    
    for i in rows:
        # print (i)

        return render_template("sales.html", rows = rows)

@app.route('/dashboard')
def dashboard():
    cur=conn.cursor()
    cur.execute (""" select sales.quantity, products.name from products join sales on sales.id=products.id group by products.name, sales.quantity;""")
    rows=cur.fetchall()

    data =[]
    labels =[]
    for i in rows:
        data.append(i[0])
        labels.append(i[1])

        print(data)

    return render_template("dashboard.html" , labesl=labels, datas=data )


@app.route('/inventory')
def inventories():
    cur= conn.cursor()
    cur.execute("""select * from products""")
    rows = cur.fetchall()

    for i in rows:
        # print (i[0])
     return render_template("inventory.html",rows=rows )

@app.route ("/view/<int:im>")
def view_sales(im):
    cur=conn.cursor()
    cur.execute("select * from sales where pid= %s",str(im))
    rows = cur.fetchall()
    # print (rows)
    return render_template("view.html", rows=rows)

if __name__ =="__main__":
    app.run(debug=True)