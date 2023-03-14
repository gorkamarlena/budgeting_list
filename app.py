from flask import Flask, jsonify, abort, make_response, Response, request
from models import expenses

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_key"

@app.route("/expenses/", methods=["GET"])
def expenses_list():
    return jsonify(expenses.all())

@app.route("/expenses/total/", methods=["GET"])
def expenses_total():
    total = 0
    for i in expenses.all():
        total += float(i['amount'])
    return jsonify(total)

@app.route("/expenses/<int:expenses_id>", methods=["GET"])
def get_expenses(expenses_id):
    expenses_record = expenses.get(expenses_id)
    if not expenses_record:
        abort(404)
    return jsonify({"expenses_record": expenses_record})

@app.route("/expenses/", methods=["POST"])
def create_expenses_record():
    if not request.json or not 'date' in request.json:
        abort(400)
    new_record = {
        'id': expenses.all()[-1]['id'] + 1,
        'date': request.json['date'],
        'category': request.json['category'],
        'description': request.json.get('description', ""),
        'amount': request.json['amount']
    }
    expenses.create(new_record)
    return Response(status=201)

@app.route("/expenses/<int:expenses_id>", methods=['DELETE'])
def delete_expenses_record(expenses_id):
    result = expenses.delete(expenses_id)
    if not result:
        abort(404)
    return Response(status=200)

@app.route("/expenses/<int:expenses_id>", methods=["PUT"])
def update_expenses_record(expenses_id):
    record = expenses.get(expenses_id)
    if not record:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'date' in data and not isinstance(data.get('date'), str),
        'category' in data and not isinstance(data.get('category'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'amount' in data and not isinstance(data.get('amount'), str)
    ]):
        abort(400)
    updated_record = {
        'id': data.get('id', record['id']),
        'date': data.get('date', record['date']),
        'category': data.get('category', record['category']),
        'description': data.get('description', record['description']),
        'amount': data.get('amount', record['amount'])
    }
    expenses.update(expenses_id, updated_record)
    return jsonify({'record': updated_record})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)
