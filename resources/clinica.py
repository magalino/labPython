from flask_restful import Resource, reqparse
from models.clinica import ClinicaModel
from flask_jwt_extended import jwt_required
import psycopg2 #postgres

# lista todos os registros do banco
class Clinicas (Resource):
    def get (self):

        connection = psycopg2.connect(user='sidney',
                                      password='123456',
                                      host='localhost',
                                      port='5432',
                                      database='postgres')
        
        cursor = connection.cursor()

        consulta = "SELECT * FROM clinicas"
        cursor.execute(consulta)
        resultado = cursor.fetchall()

        clinicas = []
        for linha in resultado:
            clinicas.append({
                'clinica_id': linha[0],
                'nome': linha[1],
                'endereco': linha[2],
                'telefone': linha[3],
                'email': linha[4],
                'googlemaps': linha[5]                
            })

        return {'clinicas': clinicas}
      
class Clinica (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'none' cannot be left blank.")
    argumentos.add_argument('endereco')  
    argumentos.add_argument('telefone')  
    argumentos.add_argument('email')  
    argumentos.add_argument('googlemaps')  

    # método GET
    def get (self, clinica_id):
        clinica = ClinicaModel.find_clinica(clinica_id)

        if clinica:
            return clinica.json(), 200 #ok
        
        return {'message': 'Clinica not found.'}, 404 #not found 
      
    # método POST
    @jwt_required()
    def post (self, clinica_id):
        
        if ClinicaModel.find_clinica(clinica_id):
            return {"message": "Clinica Id '{}' already exists." .format(clinica_id)}, 400 #bad request

        dados = Clinica.argumentos.parse_args()
        clinica = ClinicaModel(clinica_id, **dados)

        try:
            clinica.save_clinica() 
        except:
            return {'message': 'An internal error occurred trying to put clinica.'}, 500 #internal server erro
        
        return clinica.json(), 201 #criado
    
    # método PUT
    @jwt_required()
    def put (self, clinica_id):

        dados = Clinica.argumentos.parse_args()     
        clinica_encontrado = ClinicaModel.find_clinica(clinica_id)

        # update
        if clinica_encontrado:
            clinica_encontrado.update_clinica(**dados)

            try:
                clinica_encontrado.save_clinica() 
            except:
                return {'message': 'An internal error occurred trying to update clinica.'}, 500 #internal server erro

            return clinica_encontrado.json(), 200 #atualizado 
        
        # create 
        clinica = ClinicaModel(clinica_id, **dados) 

        try:
            clinica.save_clinica() 
        except:
            return {'message': 'An internal error occurred trying to create clinica.'}, 500 #internal server erro
        
        return clinica.json(), 201 #criado

    # método DELETE
    @jwt_required()
    def delete (self, clinica_id):

        clinica = ClinicaModel.find_clinica(clinica_id)

        if clinica:

            try:
                clinica.delete_clinica()
            except:    
                return {'message': 'An internal error occurred trying to delete clinica.'}, 500 #internal server erro
            
            return {'message': 'Clinica deleted.'}, 200 #ok
        
        return {'message': 'Clinica not found.'}, 404 #not found 