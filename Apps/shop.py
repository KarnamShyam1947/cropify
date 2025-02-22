from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from Models import OrderModel, ProductModel
from App import db

shop = Blueprint("shop", __name__)

@shop.route("/add-product", methods=['GET', 'POST'])
def add_product():
    # check admin access
    if request.method == 'POST':
        name = request.form.get('p-name')
        price = request.form.get('p-price')
        des = request.form.get('des')

        product = ProductModel.query.filter_by(name=name).first()

        if product:
            flash("Product all ready exists", "danger")
            return redirect(url_for('shop.add_product'))

        file = request.files.get("img")
        filename = 'static/images/products/'+secure_filename(file.filename)
        print(filename)
        file.save(filename)

        new_product = ProductModel(
            name=name,
            price=price,
            description=des,
            img_url=filename
        )

        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully", "success")
        return redirect(url_for('shop.add_product'))
        

    return render_template("shop/add-product.html")

@shop.route("/all-products")
def all_products():
    products = ProductModel.query.all()

    return render_template("shop/all-products.html", products=products)

@shop.route("/buy-product")
def buy_product():
    pid = request.args.get('pid')

    order = OrderModel(userId=session['id'], productId=pid)
    db.session.add(order)
    db.session.commit()

    flash("Order completed successfully", "success")
    return redirect(url_for("shop.products"))

@shop.route("/orders")
def products():
    orders = OrderModel.query.filter_by(userId=session['id']).all()
    products = list()

    for order in orders:
        products.append((ProductModel.query.filter_by(id=order.productId).first(), order))

    return render_template("shop/orders.html", products=products)
