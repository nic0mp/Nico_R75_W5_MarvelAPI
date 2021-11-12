from flask import Blueprint, request, jsonify

from marvelCharx.helpers import token_required
from marvelCharx.models import db,User,Character,character_schema,characters_schema

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': "value" , 
            'other': 'Data' }

# CREATE MARVEL CHARACTER ENDPOINT
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    charCreation_date = request.json['charCreation_date']
    super_power = request.json['super_power']
    team_affiliation = request.json['team_affiliation']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    character = Character(name,description,comics_appeared_in, charCreation_date,super_power,team_affiliation,user_token = user_token )
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)


# RETRIEVE ALL MARVEL CHARACTERs ENDPOINT
@api.route('/character', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    character = Character.query.filter_by(user_token = owner).all()
    response = character_schema.dump(character)
    return jsonify(response)  
    

# RETRIEVE ONE MARVEL CHARACTER ENDPOINT
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


# UPDATE MARVEL CHARACTER ENDPOINT
@api.route('/characters/<id>', methods = ['POST','PUT'])
@token_required
def update_character(current_user_token,id):
    character = Character.query.get(id) # GET DRONE INSTANCE

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.charCreation_date = request.json['charCreation_date']
    character.super_power = request.json['super_power']
    character.team_affiliation = request.json['team_affiliation']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)


# DELETE MARVEL CHARACTER ENDPOINT
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    
    response = character_schema.dump(character)
    return jsonify(response)