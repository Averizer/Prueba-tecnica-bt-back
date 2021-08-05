from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

#Config flask
app = Flask(__name__)

#Config mongodb
app.config['MONGO_URI'] = 'mongodb://localhost/pruebabt'
mongo = PyMongo(app)

#Parametrización y soporte en las rutas
CORS(app)

#Seleccionar base de datos
db = mongo.db.usuarios


#-------------------CREAR USUARIO ----------------------
@app.route('/users',methods=['POST'])
def create_user():
    print(request.json)
    id = db.insert({
        'nombre': request.json['nombre'],
        'correo': request.json['correo'],
        'edad': request.json['edad']
    })
    print(id)
    return jsonify(str(ObjectId(id)))

#------------------LISTAR USUARIOS ---------------------
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    #Se podria mapear en lugar de iterar
    for user in db.find():
        users.append({
            '_id': str(ObjectId(user['_id'])),
            'nombre': user['nombre'],
            'correo': user['correo'],
            'edad': user['edad']
        })
    return jsonify(users)

#------------------BUSCAR USUARIO ----------------------
@app.route('/user/<id>',methods=['GET'])
def get_user(id):
    user = db.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'nombre': user['nombre'],
        'correo': user['correo'],
        'edad': user['edad']
    })

#------------------BORRRAR USUARIO ---------------------
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User deleted'})

#-----------------ACTUALIZAR USUARIO -------------------
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    db.update_one({'_id': ObjectId(id)},{'$set': {
        'nombre': request.json['nombre'],
        'correo': request.json['correo'],
        'edad': request.json['edad']
    }})
    return jsonify({'msg': 'User updated'})

#+++++++++++++++++++++INCIAIALIZAR++++++++++++++++++++++
if __name__ == "__main__":
    app.run(debug=True)