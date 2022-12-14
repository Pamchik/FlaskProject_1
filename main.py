from collections import namedtuple

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Assortment.db'

app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False
db = SQLAlchemy(app)


list = namedtuple('list', 'title price')
list_all = []


class Assortment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)
# Таблица:
#  id   title   price   description   date         isActive
#  1    name1   00.00   text1         dd.mm.yyyy   True
#  2    name2   00.00   text2         dd.mm.yyyy   False
#  3    name3   00.00   text3         dd.mm.yyyy   False
#  ...


# class Basket_user(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     description = db.Column(db.Text(500), nullable=False)


    def __repr__(self):
        return self.id


@app.route('/')
@app.route('/home')
def index():
     items = Assortment.query.order_by(Assortment.price).all()
     return render_template("index.html", items=items)


@app.route("/basket-add/<int:id>", methods=['POST', 'GET'])
def basket_add(id):
    item = Assortment.query.get(id)

#    if request.method == 'POST':
#
    ititle = item.title
    iprice = item.price
#
    try:
        list_all.append(list(ititle, iprice))
        print(list_all)
        return redirect(url_for('index'))
    except:
        return "При добавлении товара в корзину произошла ошибка"
#    else:

    #return render_template("index.html")

    return redirect("/")


@app.route('/list-things')
def list_things():
    items = Assortment.query.order_by(Assortment.price).all()
    return render_template("list_things.html", items=items)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/basket')
def basket():
    return render_template("basket.html", list_all=list_all)


@app.route('/list-things/<int:id>')
def list_detail(id):
    item = Assortment.query.get(id)
    return render_template("item_detail.html", item=item)


@app.route('/list-things/<int:id>/delete')
def list_delete(id):
    item = Assortment.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/list-things')
    except:
        return 'При удалении товара произошла ошибка'


@app.route('/list-things/<int:id>/update', methods=['POST', 'GET'])
def list_update(id):
    item = Assortment.query.get(id)
    if request.method == 'POST':
        item.title = request.form['title']
        item.price = request.form['price']
        item.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/list-things')
        except:
            return "При редактировании товаров произошла ошибка"
    else:
        return render_template("item_update.html", item=item)


@app.route('/create-item', methods=['POST', 'GET'])
def create_item():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        thing = Assortment(title=title, price=price, description=description)

        try:
            db.session.add(thing)
            db.session.commit()
            return redirect('/list-things')
        except:
            return "При добавлении товара произошла ошибка"
    else:
        return render_template("create_item.html")


if __name__ == "__main__":
    app.run(debug=True)


#from main import app, db
#app.app_context().push()
#db.create_all()

#либо открываем flask shell, для этого в терминале пишем:
#flask shell
#from app import db
#db.create_all()