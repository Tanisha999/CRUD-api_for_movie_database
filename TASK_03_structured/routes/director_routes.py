from flask import Blueprint,jsonify,request
from schema import dir_schema
from extensions import db
from models.models import Director,Movies
from schema import dir_schema

director=Blueprint('director',__name__,)

#creating director
@director.route('/create_director', methods=['POST'])
def create_director():
    try:
        data = request.json
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        # Checking if director exists
        director_exists = db.session.query(db.exists().where(Director.name == name)).scalar()
        if director_exists:
            return jsonify({"message": "Director already exists.."})
        
        new_director = Director(name=name, age=age, gender=gender)
        db.session.add(new_director)
        db.session.commit()

        director_data = {'id': new_director.id, 'name': new_director.name, 'age': new_director.age, 'gender': new_director.gender}

        response_data = {"director": director_data, "message": "Director added successfully"}
     
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Getting all directors
@director.route('/get_directors', methods=['GET'])
def  get_directors():
    all_directors = Director.query.all()
    result = dir_schema.directors_schema.dump(all_directors)
    return jsonify(result)

# Getting director by id
@director.route('/get_director/<int:id>', methods=['GET'])
def get_director_by_id(id):
    try:
        director = Director.query.get(id)
        if director:
            return dir_schema.jsonify(director)
        else:
            return jsonify({"success": False, "message": "Director not found"})
        
    except Exception as e:
        return jsonify({"error": str(e)})

# Getting directors by name
@director.route('/get_director/<string:partial_name>', methods=['GET'])
def get_directors_by_partial_name(partial_name):
    try:
        # Perform a case-sensitive search for directors with names containing the provided partial name
        directors = Director.query.filter(Director.name.like(f"%{partial_name}%")).all()

        if directors:
            return dir_schema.directors_schema.jsonify(directors)
        else:
            return jsonify({"message": f"No directors with name containing '{partial_name}' found"})

    except Exception as e:
        return jsonify({"error": str(e)})
    

# deleting director by id along with the movies
@director.route('/delete_director/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    try:
        director = Director.query.get(director_id)
        if director:
            # Delete associated movies
            Movies.query.filter_by(director_id=director_id).delete()

            db.session.delete(director)
            db.session.commit()

            return jsonify({"message": "Director and associated movies deleted successfully"})
        else:
            return jsonify({"message": "Director not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "An error occurred."})
    
     
# updating director by id
@director.route('/update_director/<int:director_id>',methods=['PUT'])
def update_director(director_id):
     try:
          director=Director.query.get(director_id)
          if director:
               name=request.json['name']
               age=request.json['age']
               gender=request.json['gender']

               director.name=name
               director.age=age
               director.gender=gender

               db.session.commit()

               return dir_schema.jsonify(director)
          else:
               return jsonify({"error" : "director not found"})
     except Exception as e:
            return jsonify({"success": False, "error": str(e), "message": "An error occurred."}) 
     