import mysql.connector

class Config:
    
    def connect(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            port = '3306'
        )
        
    def close(self):
        self.connection.close()
        
        # self.connection.commit()

class UserDatabase(Config):
    def __init__(self,route) -> None:
        super().__init__()
        self.route = route
        
    def registrarUsuario(self,datos):
        use = 'USE MetaClr'
        camposTabla = ('Nombre,nickname,contrasenia,TMB')
        qntd = ('%s, %s, %s, %s')
        sql = f'INSERT INTO Usuario({camposTabla}) VALUES ({qntd})'
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql,datos)
        self.connection.commit()
        return 'introducido'
    
    def verificarLogin(self,datos):
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        consulta = " SELECT Nickname, contrasenia FROM Usuario WHERE Nickname = %s "
        cursor.execute(use)
        cursor.execute(consulta, (datos[0],))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            print('Usuario encontrado VL')
            return resultado[0]
        else:
            return None
        
class FoodDatabase(Config):
    def __init__(self,route) -> None:
        super().__init__()
        self.route = route
    
    def ObtenerAlimentos(self,dato):
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        cursor.execute(use)
        sql = "SELECT Alimento, Categoria FROM alimentos WHERE Alimento LIKE %s"
        cursor.execute(sql, (f'%{dato}%',))
        return cursor.fetchall()