from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
# Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # drone = db.relationship('Drone', backref = 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Numeric(precision=10,scale=2))
    charCreation_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    super_power = db.Column(db.String(100), nullable = True)
    team_affiliation = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
 

    def __init__(self,name,description,comics_appeared_in, charCreation_date,super_power,team_affiliation,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.charCreation_date = charCreation_date
        self.super_power = super_power
        self.team_affiliation = team_affiliation
        self.user_token = user_token


    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f'The following Character has been added: {self.name}'


# Creation of API Schema via the Marshmallow Object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'comics_appeared_in', 'charCreation_date', 'super_power', 'team_affiliation']


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)
