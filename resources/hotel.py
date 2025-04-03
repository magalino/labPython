from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
#import sqlite3
import psycopg2 #postgres

# path params
# path_params = reqparse.RequestParser()
# path_params.add_argument('hotel_id', type=str)
# path_params.add_argument('nome', type=str)
# path_params.add_argument('endereco', type=str)
# path_params.add_argument('limit', type=float)
# path_params.add_argument('offset', type=float)

# lista todos os registros do banco
class Hoteis (Resource):
    def get (self):

        #sqlite3
        #db_path = "C:/Users/Sidney/Downloads/pythonteste/instance/banco.db"
        #connection = sqlite3.connect(db_path)

        connection = psycopg2.connect(user='sidney',
                                      password='123456',
                                      host='localhost',
                                      port='5432',
                                      database='postgres')
        
        cursor = connection.cursor()

        #dados = path_params.parse_args()
        consulta = "SELECT * FROM hoteis WHERE nome LIKE 'hote%'"
        cursor.execute(consulta)
        resultado = cursor.fetchall()

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'endereco': linha[2]
            })

        return {'hoteis': hoteis}
    
        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}, 200 #select * from hoteis    
    
class Hotel (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'none' cannot be left blank.")
    argumentos.add_argument('endereco')  

    # método GET
    def get (self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json(), 200 #ok
        
        return {'message': 'Hotel not found.'}, 404 #not found 
      
    # método POST
    @jwt_required()
    def post (self, hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel Id '{}' already exists." .format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel() 
        except:
            return {'message': 'An internal error occurred trying to put hotel.'}, 500 #internal server erro
        
        return hotel.json(), 201 #criado
    
    # método PUT
    @jwt_required()
    def put (self, hotel_id):

        dados = Hotel.argumentos.parse_args()     
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        # update
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)

            try:
                hotel_encontrado.save_hotel() 
            except:
                return {'message': 'An internal error occurred trying to update hotel.'}, 500 #internal server erro

            return hotel_encontrado.json(), 200 #atualizado 
        
        # create 
        hotel = HotelModel(hotel_id, **dados) 

        try:
            hotel.save_hotel() 
        except:
            return {'message': 'An internal error occurred trying to create hotel.'}, 500 #internal server erro
        
        return hotel.json(), 201 #criado

    # método DELETE
    @jwt_required()
    def delete (self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:

            try:
                hotel.delete_hotel()
            except:    
                return {'message': 'An internal error occurred trying to delete hotel.'}, 500 #internal server erro
            
            return {'message': 'Hotel deleted.'}, 200 #ok
        
        return {'message': 'Hotel not found.'}, 404 #not found 