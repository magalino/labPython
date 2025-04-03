from sql_alchemy import banco

class UsuarioModel (banco.Model):

    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True)
    login= banco.Column(banco.String(40))
    senha= banco.Column(banco.String(40))

    #construtor
    def __init__(self, login, senha):
        #self.usuario_id = usuario_id #id será criado automaticamente por sequence
        self.login = login
        self.senha = senha

    def json(self):
        return{
            'usuario_id': self.usuario_id,
            'login': self.login
        }    

    @classmethod
    def find_usuario(cls, usuario_id):
        usuario = cls.query.filter_by(usuario_id=usuario_id).first() #select * from usuarios where usuario_id = <usuario_id>
        if usuario:
            return usuario
        return None
    
    @classmethod
    def find_by_login(cls, login):
        usuario = cls.query.filter_by(login=login).first() #select * from usuarios where login = <login>
        if usuario:
            return usuario
        return None    

    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()     