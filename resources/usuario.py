from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac

# variaves e funcoes globais
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")    

class Usuario (Resource):

    # /usuarios/{usuario_id}

    # método GET
    def get (self, usuario_id):
        usuario = UsuarioModel.find_usuario(usuario_id)

        if usuario:
            return usuario.json(), 200 #ok
        
        return {'message': 'User not found.'}, 404 #not found 
    
    # método DELETE
    @jwt_required()
    def delete (self, usuario_id):

        usuario = UsuarioModel.find_usuario(usuario_id)

        if usuario:

            try:
                usuario.delete_usuario()
            except:    
                return {'message': 'An internal error occurred trying to delete user.'}, 500 #internal server erro
            
            return {'message': 'User deleted.'}, 200 #ok
        
        return {'message': 'User not found.'}, 404 #not found 

class UsuarioRegister (Resource):

    # /cadastro

    def post(self):
        
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}
        
        usuario = UsuarioModel(**dados)

        try:
            usuario.save_usuario()
        except:    
            return {'message': 'An internal error occurred trying to create user.'}, 500 #internal server erro

        return {'message': 'User created successfully.'}, 201 #criado
    
class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        usuario = UsuarioModel.find_by_login(dados['login'])
        if usuario and hmac.compare_digest(usuario.senha, dados['senha']): 
            token_de_acesso = create_access_token(identity=usuario.usuario_id)
            return {'access_token': token_de_acesso},200
        return {'message': 'The username or password is incorrect.'}, 401 #unauthorized
    
class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Looged out successfully.'}