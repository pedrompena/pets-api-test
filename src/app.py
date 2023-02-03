import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Clients, Pets, Services, Contracts, Messages, Images


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Clients.query.all()
    results = [client.serialize() for client in clients]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Clients.query.get(client_id)
    result = client.serialize()
    response_body = {'message': 'OK',
                     'result': result}
    return jsonify(response_body), 200


@app.route('/clients', methods=['POST'])
def register_client():
    request_body = request.get_json()
    client = Clients(roles = request_body['roles'],
                     name = request_body['name'],
                     surname = request_body['surname'],
                     email = request_body['email'],
                     password = request_body['password'],
                     avatar = request_body['avatar'],
                     description = request_body['description'],
                     city = request_body['city'])
    db.session.add(client)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Clients.query.get(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify('OK'), 200


@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Clients.query.get(client_id)
    if client is None:
        return 'Not found', 404

    client.roles = request.json.get('roles', client.roles)
    client.name = request.json.get('name', client.name)
    client.surname = request.json.get('surname', client.surname)
    client.email = request.json.get('email', client.email)
    client.password = request.json.get('password', client.password)
    client.avatar = request.json.get('avatar', client.avatar)
    client.description = request.json.get('description', client.description)
    client.city = request.json.get('city', client.city)
    db.session.commit()

    response_body = {'roles': client.roles,
                     'name': client.name,
                     'surname': client.surname,
                     'email': client.email,
                     'password': client.password,
                     'avatar': client.avatar,
                     'description': client.description,
                     'city': client.city}

    return jsonify(response_body), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
