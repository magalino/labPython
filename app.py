from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioRegister, UsuarioLogin, UsuarioLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import banco

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sidney:123456@localhost:5432/postgres' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api (app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    app.before_request_funcs[None].remove(cria_banco)
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401 #unauthorized

#Classes em uso    
api.add_resource (Hoteis,'/hoteis')
api.add_resource (Hotel, '/hoteis/<string:hotel_id>')
api.add_resource (Usuario, '/usuarios/<int:usuario_id>')
api.add_resource (UsuarioRegister, '/cadastro')
api.add_resource (UsuarioLogin, '/login')
api.add_resource (UsuarioLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)