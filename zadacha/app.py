from flask import Flask, request, jsonify, redirect
from flask_restx import Api, Resource, fields, Namespace
from models import db, Item, ItemSchema, Marshmallow
from config import Config
ma=Marshmallow() #вроде в моделях прописан но выдает ошибку без этого

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

api = Api(app, 
          version='1.0', 
          title='Почему все это называется итемы?',
          description='что тут писать?',
          doc='/docs')

ns=Namespace('items', description='Tut objecti')
api.add_namespace(ns)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect('/docs')  # Перенаправление на /docs блять не работает но я слишком заебался

item_model = ns.model('Item', {
    'id': fields.Integer(readOnly=True, description='Идентификатор элемента'),
    'name': fields.String(required=True, description='Название элемента'),
    'description': fields.String(description='Описание элемента'),
    'price': fields.Float(required=True, description='Цена элемента'),
    'created_at': fields.DateTime(readOnly=True, description='Время создания')
})

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
@ns.route('/')
class ItemList(Resource):
    @ns.doc('list_items')
    @ns.marshal_list_with(item_model)
    def get(self):
        '''Список'''
        items = Item.query.all()
        return items_schema.dump(items)

    @ns.doc('create_item')
    @ns.expect(item_model, validate=True)
    @ns.marshal_with(item_model, code=201)
    def post(self):
        '''создание нового элемента'''
        new_item = Item(
            name=request.json['name'],
            description=request.json.get('description', ''),
            price=request.json['price']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201

@ns.route('/<int:item_id>')
@ns.param('item_id', 'Ид')
class ItemResource(Resource):
    @ns.doc('get_item')
    @ns.marshal_with(item_model)
    def get(self, item_id):
        '''Получение элемента по ID'''
        item = Item.query.get_or_404(item_id)
        return item_schema.dump(item)

    @ns.doc('update_item')
    @ns.expect(item_model, validate=True)
    @ns.marshal_with(item_model)
    def put(self, item_id):
        '''Обновление элемента по ID'''
        item = Item.query.get_or_404(item_id)
        item.name = request.json.get('name', item.name)
        item.description = request.json.get('description', item.description)
        item.price = request.json.get('price', item.price)
        db.session.commit()
        return item_schema.dump(item)

    @ns.doc('delete_item')
    def delete(self, item_id):
        '''удаление элемента по ID'''
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item удале'}, 204

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)