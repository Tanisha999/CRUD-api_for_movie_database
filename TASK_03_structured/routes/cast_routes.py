from flask import Blueprint,request,jsonify
from extensions import db
from models.models import CastMember
from schema import cast_schema

cast=Blueprint('cast',__name__,)

# Creating a cast member
@cast.route('/create_cast_member', methods=['POST'])
def create_cast_member():
    try:
        data = request.json
        name = data.get('name')

        # Checking if cast member exists
        cast_member_exists = CastMember.query.filter_by(name=name).first()
        if cast_member_exists:
            return jsonify({"message": "Cast member already exists."})

        new_cast_member = CastMember(name=name)
        db.session.add(new_cast_member)
        db.session.commit()

        cast_member_data = {'id': new_cast_member.id, 'name': new_cast_member.name}

        response_data = {"cast_member": cast_member_data, "message": "Cast member added successfully"}

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})
    
#updating cast member
@cast.route('/update_cast_member/<int:id>',methods=['PUT'])
def update_cast_member(id):
    try:
        cast_member=CastMember.query.get(id)
        if cast_member:
            name=request.json['name']

            cast_member.name=name

            db.session.commit()

            return cast_schema.jsonify(cast_member)
        else:
            return jsonify({"message" : "Member not found"})
        
    except Exception as e:
        return jsonify({"error" : str(e)})
    
    