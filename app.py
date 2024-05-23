from flask import Flask, request, jsonify, render_template, redirect, url_for
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import os


app = Flask(__name__)

account_name = 'labnttstg01'
account_key = 'Tt+K676XDKVRqG9M+PU36HG9yz7iuPlLXaEIB5Wssx5f6iWrl4WtpMb/kkFzRuI3bMNtLlhwTZqs+AStySH+Vw=='
table_service = TableService(account_name=account_name, account_key=account_key)

# Crear la tabla si no existe
table_name = 'ShoppingList'
if not table_service.exists(table_name):
    table_service.create_table(table_name)

@app.route('/')
def home():
    items = table_service.query_entities(table_name, filter="PartitionKey eq 'shopping'")
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.form.get('item')
    quantity = request.form.get('quantity')
    if item and quantity:
        new_item = Entity()
        new_item.PartitionKey = 'shopping'
        new_item.RowKey = item
        new_item.quantity = int(quantity)
        table_service.insert_or_replace_entity(table_name, new_item)
    return redirect(url_for('home'))

@app.route('/get_list', methods=['GET'])
def get_list():
    items = table_service.query_entities(table_name, filter="PartitionKey eq 'shopping'")
    return jsonify([{'item': item.RowKey, 'quantity': item.quantity} for item in items])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
