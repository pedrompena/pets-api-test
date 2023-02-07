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
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


#  CLIENTS


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
    client = Clients(roles=request_body['roles'],
                     name=request_body['name'],
                     surname=request_body['surname'],
                     email=request_body['email'],
                     password=request_body['password'],
                     avatar=request_body['avatar'],
                     description=request_body['description'],
                     city=request_body['city'])
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


# PETS


@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pets.query.all()
    results = [pet.serialize() for pet in pets]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = Pets.query.get(pet_id)
    if pet is None:
        return 'Not found', 404
    result = pet.serialize()
    response_body = {'message': 'OK',
                     'result': result}
    return jsonify(response_body), 200


@app.route('/pets', methods=['POST'])
def register_pet():
    request_body = request.get_json()
    pet = Pets(name=request_body['name'],
               image=request_body['image'],
               description=request_body['description'],
               owner_id=request_body['owner_id'])
    db.session.add(pet)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = Pets.query.get(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify('OK'), 200


@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet = Pets.query.get(pet_id)
    if pet is None:
        return 'Not found', 404

    pet.name = request.json.get('name', pet.name)
    pet.image = request.json.get('image', pet.image)
    pet.description = request.json.get('description', pet.description)

    db.session.commit()

    response_body = {'id': pet.id,
                     'name': pet.name,
                     'image': pet.image,
                     'description': pet.description,
                     'owner_id': pet.owner_id}

    return jsonify(response_body), 200


# SERVICES


@app.route('/services', methods=['GET'])
def get_services():
    services = Services.query.all()
    results = [service.serialize() for service in services]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Services.query.get(service_id)
    if service is None:
        return 'Not found', 404
    result = service.serialize()
    response_body = {'message': 'OK',
                     'result': result}
    return jsonify(response_body), 200


@app.route('/services', methods=['POST'])
def register_service():
    request_body = request.get_json()
    service = Services(title=request_body['title'],
                       price=request_body['price'],
                       description=request_body['description'],
                       carer_id=request_body['carer_id'])
    db.session.add(service)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Services.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify('OK'), 200


@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Services.query.get(service_id)
    if service is None:
        return 'Not found', 404

    service.title = request.json.get('title', service.title)
    service.price = request.json.get('price', service.price)
    service.description = request.json.get('description', service.description)
    service.carer_id = request.json.get('carer_id', service.carer_id)

    db.session.commit()

    response_body = {'id': service.id,
                     'title': service.title,
                     'price': service.price,
                     'description': service.description,
                     'carer_id': service.carer_id}

    return jsonify(response_body), 200


# CONTRACTS


@app.route('/contracts', methods=['GET'])
def get_contracts():
    contracts = Contracts.query.all()
    results = [contract.serialize() for contract in contracts]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@app.route('/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    contract = Contracts.query.get(contract_id)
    if contract is None:
        return 'Not found', 404
    result = contract.serialize()
    response_body = {'message': 'OK',
                     'result': result}
    return jsonify(response_body), 200


@app.route('/contracts', methods=['POST'])
def register_contract():
    request_body = request.get_json()
    contract = Contracts(pet_id=request_body['pet_id'],
                         service_id=request_body['service_id'],
                         date=request_body['date'],
                         price=request_body['price'])
    db.session.add(contract)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    contract = Contracts.query.get(contract_id)
    db.session.delete(contract)
    db.session.commit()
    return jsonify('OK'), 200


@app.route('/contracts/<int:contract_id>', methods=['PUT'])
def update_contract(contract_id):
    contract = Contracts.query.get(contract_id)
    if contract is None:
        return 'Not found', 404

    contract.pet_id = request.json.get('pet_id', contract.pet_id)
    contract.service_id = request.json.get('service_id', contract.service_id)
    contract.date = request.json.get('date', contract.date)
    contract.price = request.json.get('price', contract.price)
    contract.assessment = request.json.get('assessment', contract.assessment)
    contract.comments = request.json.get('comments', contract.comments)

    db.session.commit()

    response_body = {'id': contract.id,
                     'pet_id': contract.pet_id,
                     'service_id': contract.service_id,
                     'date': contract.date,
                     'price': contract.price,
                     'assessment': contract.assessment,
                     'comments': contract.comments}

    return jsonify(response_body), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
