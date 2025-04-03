from sql_alchemy import banco

class HotelModel (banco.Model):

    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key = True)
    nome= banco.Column(banco.String(50))
    endereco= banco.Column(banco.String(100))

    #construtor
    def __init__(self, hotel_id, nome, endereco):
        self.hotel_id = hotel_id
        self.nome = nome
        self.endereco = endereco

    def json(self):
        return{
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'endereco': self.endereco
        }    

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #select * from hoteis where hotel_id = <hotel_id>
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()