import os
import pymongo


from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myfirstcluster"
COLLECTION = "inventory_manager"


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'inventory_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/solvents')
def solvents():
    return render_template("solvents.html", solvents=mongo.db.solvents.find())


@app.route('/consumables')
def consumables():
    return render_template("consumables.html", consumables=mongo.db.consumables.find())


@app.route('/request_table')
def request_table():
    return render_template("request_table.html")


@app.route('/addsolvents')
def addsolvents():
    return render_template("addsolvents.html")


@app.route('/solquantchange/<solvent_id>')
def solquantchange(solvent_id):
    the_solvent = mongo.db.solvents.find_one({"_id": ObjectId(solvent_id)})
    return render_template('solquantchange.html', solvent=the_solvent)


@app.route('/solchange/<solvent_id>', methods=["POST"])
def solchange(solvent_id):
    mongo.db.solvents.update({'_id': ObjectId(solvent_id)},
    {
        'Name': request.form.get('Name'),
        'Supplier': request.form.get('Supplier'),
        'Cat_no': request.form.get('Cat_no'),
        'Grade': request.form.get('Grade'),
        'Min_Quantity': request.form.get('Min_Quantity'),
        'Quantity_Available': request.form.get('Quantity_Available'),
        'Quantity_Unit': request.form.get('Quantity_Unit'),
        'Price': request.form.get('Price'),
        'Currency': request.form.get('Currency'),
        'Comment': request.form.get('Comment')
    })
    return redirect(url_for('solvents'))


@app.route('/addsolvents', methods=['POST'])
def addsolvents_add():
    solvents = mongo.db.solvents
    solvents.insert_one(request.form.to_dict())
    return redirect(url_for('solvents'))


@app.route('/addconsumables')
def addconsumables():
    return render_template("addconsumables.html")


@app.route('/addconsumables', methods=['POST'])
def addconsumables_add():
    consumables = mongo.db.consumables
    consumables.insert_one(request.form.to_dict())
    return redirect(url_for('consumables'))


@app.route('/conquantchange/<consumable_id>')
def conquantchange(consumable_id):
    con = mongo.db.consumables.find_one({"_id": ObjectId(consumable_id)})
    return render_template('conquantchange.html', consumable=con)


@app.route('/conchange/<consumable_id>', methods=["POST"])
def conchange(consumable_id):
    mongo.db.consumables.update({'_id': ObjectId(consumable_id)},
    {
        'Name': request.form.get('Name'),
        'Supplier': request.form.get('Supplier'),
        'Cat_no': request.form.get('Cat_no'),
        'Min_Quantity': request.form.get('Min_Quantity'),
        'Quantity_Available': request.form.get('Quantity_Available'),
        'Quantity_Unit': request.form.get('Quantity_Unit'),
        'Price': request.form.get('Price'),
        'Currency': request.form.get('Currency'),
    })
    return redirect(url_for('consumables'))


@app.route('/deletesolvent')
def deletesolvent():
    return render_template('deletesolvent.html')


@app.route('/deletesolvent/<sol_id>')
def deletesolvent_delete(sol_id):
    mongo.db.solvents.remove({'_id': ObjectId(sol_id)})
    return redirect(url_for('solvents'))


@app.route('/deleteconsumable')
def deleteconsumable():
    return render_template('deleteconsumable.html')


@app.route('/deleteconsumable/<cid>')
def deleteconsumable_delete(cid):
    mongo.db.consumables.remove({'_id': ObjectId(cid)})
    return render_template('consumables.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)