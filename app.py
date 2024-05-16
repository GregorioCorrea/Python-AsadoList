from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Lista de compras en memoria
shopping_list = []

@app.route('/')
def home():
    return render_template('index.html', items=shopping_list)

@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.form.get('item')
    if item:
        shopping_list.append(item)
    return redirect(url_for('home'))

@app.route('/get_list', methods=['GET'])
def get_list():
    return jsonify(shopping_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)