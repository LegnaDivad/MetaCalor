import mysql.connector

class Config:
    def __init__(self,route) -> None:
        self.route = route
    
    # def connect(self):
    #     self.connection = mysql.connector.connect(
    #         host="137.184.234.157",
    #         user="Cucei_Co_Us",
    #         password="UscuceiCom7707",
    #         database="Cucei_Comparte",
    #         port="3306"
    #     )
    
    def connect(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            port = '3307'
        )
        
    def close(self):
        self.connection.close()
        
        
class UserDatabase(Config):
    def __init__(self, route) -> None:
        super().__init__(route)
    
    def login(self,datos):
        cursor = self.connection.cursor()
        use = 'USE CuceiComparte'
        consulta = "SELECT Nombre_Usuario,Contraseña,ID_usuario FROM Usuarios WHERE Nombre_Usuario = %s AND Contraseña = %s"
        cursor.execute(use)
        cursor.execute(consulta, (datos[0],datos[1],))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            print('Usuario Encontrado')
            return resultado[2]
        else:
            return None
        
    def ObtenerUsuario(self,id):
        cursor = self.connection.cursor()
        use = 'USE CuceiComparte'
        consulta = "SELECT Nombre_Usuario FROM Usuarios WHERE ID_usuario = %s"
        cursor.execute(use)
        cursor.execute(consulta, (id,))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            print('Usuario Encontrado')
            return resultado[0]
        else:
            return None
    
class ProductDatabase(Config):
    def __init__(self, route) -> None:
        super().__init__(route)
        
    def seleccionarProductos(self):
        use = 'USE CuceiComparte'
        cursor = self.connection.cursor()
        sql =  """SELECT P.Titulo_producto AS Nombre_producto, P.Precio, U.Nombre_usuario AS Nombre_usuario_subio
                FROM Productos AS P
                JOIN Usuarios AS U ON P.ID_usuario_subio = U.ID_usuario"""
        cursor.execute(use)
        cursor.execute(sql)
        return cursor.fetchall()
    
    def seleccionarProductosDeUsuario(self,id):
        use = 'USE CuceiComparte'
        cursor = self.connection.cursor()
        sql =  """SELECT P.Titulo_producto AS Nombre_producto, P.Precio, U.Nombre_usuario AS Nombre_usuario_subio
                FROM Productos AS P
                JOIN Usuarios AS U ON P.ID_usuario_subio = U.ID_usuario
                WHERE P.ID_usuario_subio = %s"""
        cursor.execute(use)
        cursor.execute(sql, (id,))
        return cursor.fetchall()
        
    def registrarProducto(self,datos):
        use = 'USE CuceiComparte'
        
        camposTabla = ('Titulo_producto, Precio, Categoria_producto, ID_usuario_subio')
        qntd = ('%s, %s, %s, %s')
        sql = f"INSERT INTO Productos({camposTabla}) VALUES ({qntd})"
        
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql,datos)
        self.connection.commit()
        return 'introducido'