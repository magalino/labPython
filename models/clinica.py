from sql_alchemy import banco

class ClinicaModel (banco.Model):

    __tablename__ = 'clinicas'
    clinica_id = banco.Column(banco.String, primary_key = True)
    nome= banco.Column(banco.String(50))
    endereco= banco.Column(banco.String(100))
    telefone= banco.Column(banco.String(50))
    email= banco.Column(banco.String(50))
    googlemaps= banco.Column(banco.String(100))

    #construtor
    def __init__(self, clinica_id, nome, endereco, telefone, email, googlemaps):
        self.clinica_id = clinica_id
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.googlemaps = googlemaps

    def json(self):
        return{
            'clinica_id': self.clinica_id,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'googlemaps': self.googlemaps
        }    

    @classmethod
    def find_clinica(cls, clinica_id):
        clinica = cls.query.filter_by(clinica_id=clinica_id).first()
        if clinica:
            return clinica
        return None
    
    def save_clinica(self):
        banco.session.add(self)
        banco.session.commit()

    def update_clinica(self, nome, endereco, telefone, email, googlemaps):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.googlemaps = googlemaps

    def delete_clinica(self):
        banco.session.delete(self)
        banco.session.commit()