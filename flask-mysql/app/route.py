from flask import Blueprint, request, jsonify, make_response
from . import db

routes = Blueprint('routes', __name__)


@routes.route('/test', methods=['GET'])
def test():
    return 'Route is working'

@routes.route('/authors', methods=['GET'])
def get_all_authors():
    try:
        from .authors_models import AuthorSchema, Author
        all_authors = Author.query.all()
        author_schema = AuthorSchema(many=True)
        result = author_schema.dump(all_authors)
        return make_response(jsonify({"authors": result}), 200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@routes.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    try:
        from .authors_models import AuthorSchema, Author
        get_authors_with_id = Author.query.get(id)
        # Handling if the id is not found/not exist
        if not get_authors_with_id:
            return jsonify({"error": "Aauthor not found"}), 404
        
        #serialise author to json
        author_schema = AuthorSchema()
        result = author_schema.dump(get_authors_with_id)
        return make_response(jsonify({"authors": result}), 200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/authors', methods=['POST'])
def create_author():
    try:
        from .authors_models import AuthorSchema, Author
        data = request.get_json()

        author_schema = AuthorSchema()
        new_author = author_schema.load(data)
        db.session.add(new_author)
        db.session.commit()
        result = author_schema.dump(new_author)
        return make_response(jsonify({"authors": result}), 201)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@routes.route('/authors/<int:id>', methods=['PUT'])
def update_authors_by_id(id):
    try: 
        from .authors_models import AuthorSchema, Author
        data = request.get_json()
        get_author = Author.query.get(id)
        if not get_author:
            return jsonify({"error": "uthors ID not found"}), 404
        if data.get('name'):
            get_author.name = data['name']
        if data.get('specialisation'):
            get_author.specialisation = data['specialisation']
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema(only=['id', 'name', 'specialisation'])
        result = author_schema.dump(get_author)
        return make_response(jsonify({"authors": result}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@routes.route('/authors/<int:id>', methods=['DELETE'])
def delete_author_by_id(id):
    try:

        from .authors_models import Author
        get_author = Author.query.get(id)

        if not get_author:
            return jsonify({"error": "Author ID not found"}), 404
        db.session.delete(get_author)
        db.session.commit()
        return make_response("", 204)
    except Exception as e:
        return jsonify({"error": str(e)}), 500