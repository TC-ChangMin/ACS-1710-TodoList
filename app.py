from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/todoList"
mongo = PyMongo(app)
todo_items = mongo.db.todo_items

############################################################
# ROUTES
############################################################


@app.route('/', methods=['GET'])
def seeList():

    items = list(todo_items.find())
    context = {
        'todo_items': items
    }
    return render_template('list.html', **context)

@app.route('/add', methods=['GET', 'POST'])
def addToList():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        todo_items.insert_one({'name': item_name})
        return redirect(url_for('seeList'))
    return render_template('add.html')

@app.route('/delete/<item_id>', methods=['POST'])
def deleteItem(item_id):
    todo_items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('seeList'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

