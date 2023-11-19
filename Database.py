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
        # return 'introducido'
        return not None
    
    def verificarLogin(self,datos):
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        consulta = " SELECT Nickname, contrasenia,ID_Usuario FROM Usuario WHERE Nickname = %s AND contrasenia = %s"
        cursor.execute(use)
        cursor.execute(consulta, (datos[0],datos[1],))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            print('Usuario encontrado VL')
            return resultado
        else:
            return None
        
    def ObtenerRegistros(self,id):
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        cursor.execute(use)
        sql = '''SELECT A.Alimento,RA.Total_Calorias,RA.Horario 
        FROM registro_alimentos AS RA
        JOIN Alimentos AS A ON A.ID_Alimento = RA.ID_Alimento
        WHERE RA.ID_Usuario = %s'''
        cursor.execute(sql, (id,))
        return cursor.fetchall()
        
class FoodDatabase(Config):
    def __init__(self,route) -> None:
        super().__init__()
        self.route = route
    
    def ObtenerAlimentos(self,dato):
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        cursor.execute(use)
        sql = "SELECT Alimento, Categoria,Unidad,Cantidad,Energia_kcal,Proteina_g,Lipidos_g,Hidratos_de_carbono_g,Peso_bruto_g,ID_Alimento FROM alimentos WHERE Alimento LIKE %s"
        cursor.execute(sql, (f'%{dato}%',))
        return cursor.fetchall()
    
    def registrarAlimentoDia(self,datos):
        use = 'USE MetaClr'
        camposTabla = ('ID_Usuario,ID_Alimento,Fecha_registro,Total_calorias,horario')
        qntd = ('%s, %s, %s, %s, %s')
        sql = f'INSERT INTO Registro_Alimentos({camposTabla}) VALUES ({qntd})'
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql,datos)
        self.connection.commit()
        # return 'introducido'
        return not None