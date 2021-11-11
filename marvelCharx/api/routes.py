from flask import Blueprint, request, jsonify

from marvelCharx.helpers import token_required
from marvelCharx.models import db,User,Drone,drone_schema,drones_schema

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': "value" , 
            'other': 'Data' }

# CREATE MARVEL CHARACTER ENDPOINT
@api.route('/drones', methods = ['POST'])
@token_required
def create_drone(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    charCreation_date = request.json['charCreation_date']
    super_power = request.json['super_power']
    team_affiliation = request.json['team_affiliation']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    drone = Drone(name,description,comics_appeared_in, charCreation_date,super_power,team_affiliation,user_token = user_token )
    db.session.add(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)


# RETRIEVE ALL MARVEL CHARACTERs ENDPOINT
@api.route('/drones', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = drones_schema.dump(drones)
    return jsonify(response)  
    

# RETRIEVE ONE MARVEL CHARACTER ENDPOINT
@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_drone(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        drone = Drone.query.get(id)
        response = drone_schema.dump(drone)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


# UPDATE MARVEL CHARACTER ENDPOINT
@api.route('/drones/<id>', methods = ['POST','PUT'])
@token_required
def update_drone(current_user_token,id):
    drone = Drone.query.get(id) # GET DRONE INSTANCE

    drone.name = request.json['name']
    drone.description = request.json['description']
    drone.comics_appeared_in = request.json['comics_appeared_in']
    drone.charCreation_date = request.json['charCreation_date']
    drone.super_power = request.json['super_power']
    drone.team_affiliation = request.json['team_affiliation']
    drone.user_token = current_user_token.token

    db.session.commit()
    response = drone_schema.dump(drone)
    return jsonify(response)


# DELETE MARVEL CHARACTER ENDPOINT
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    drone = Drone.query.get(id)
    db.session.delete(drone)
    db.session.commit()
    
    response = drone_schema.dump(drone)
    return jsonify(response)