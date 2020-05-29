from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()  # parses incoming jsons, ensure that 'price' field is included in json payload
    parser.add_argument('price', type=float, required=True, help="This field can't be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    @jwt_required() #authentication required to use get
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item with name {name} already exists.'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data) #unpack dictionary
        try:
            item.save_to_db()
        except Exception:
            return {"message": "Error occured while inserting item."}, 500 #500 is internal server error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
