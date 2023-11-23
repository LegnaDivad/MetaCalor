import mysql.connector

class Config:
    # def connect(self):
    #     self.connection = mysql.connector.connect(
    #         host = 'localhost',
    #         user = 'root',
    #         password = '',
    #         port = '3306'
    #     )
    def connect(self):
        self.connection = mysql.connector.connect(
            host = '137.184.234.157',
            user = 'metaclrlng23',
            password = 'Clr23BX',
            database = 'metaclr',
            port = '3306'
        )
        
    def close(self):
        self.connection.close()

class UserDatabase(Config):
    def __init__(self,route) -> None:
        super().__init__()
        self.route = route
        
    def registrarUsuario(self,datos):
        use = 'USE metaclr'
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
        use = 'USE metaclr'
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
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT A.Alimento,RA.Total_Calorias,RA.Horario,RA.Total_proteinas,RA.Total_lipidos,RA.Total_hidratos 
        FROM Registro_Alimentos AS RA
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
        use = 'USE metaclr'
        cursor.execute(use)
        sql = "SELECT Alimento, Categoria,Unidad,Cantidad,Energia_kcal,Proteina_g,Lipidos_g,Hidratos_de_carbono_g,Peso_bruto_g,ID_Alimento FROM Alimentos WHERE Alimento LIKE %s"
        cursor.execute(sql, (f'%{dato}%',))
        return cursor.fetchall()
    
    def registrarAlimentoDia(self,datos):
        use = 'USE metaclr'
        camposTabla = ('ID_Usuario,ID_Alimento,Fecha_registro,Total_calorias,Total_lipidos,Total_hidratos,Total_proteinas,horario')
        qntd = ('%s, %s, %s, %s, %s, %s, %s, %s')
        sql = f'INSERT INTO Registro_Alimentos({camposTabla}) VALUES ({qntd})'
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql,datos)
        self.connection.commit()
        # return 'introducido'
        return not None