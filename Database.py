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

class generalDatabaseAccess(Config):
    def __init__(self,route) -> None:
        super().__init__()
        self.route = route
    
    #el ultimo parametro es la cantidad de datos que queremos recuperar
    def recuperarRegistro(self, campos_select, tabla_from, condiciones_where, cantidad=0):
        try:
            with self.connection.cursor() as cursor:
                consulta = f"SELECT {campos_select} FROM {tabla_from} WHERE {condiciones_where}"
                cursor.execute(consulta)
        
                if cantidad == 0:
                    return cursor.fetchall()
                else:
                    resultados = [cursor.fetchone() for _ in range(cantidad)]
                    return resultados

        except Exception as e:
            print(f"Error al recuperar registros: {e}")
        return None
    
    def insertarRegistro(self, tabla_from, valores_insertados, condiciones_where):
        try:
            with self.connection.cursor() as cursor:
                consulta = f"INSERT INTO {tabla_from} {valores_insertados} VALUES {condiciones_where}"
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al insertar registro/s: {e}")
    
    def modificarRegistro(self, tabla_from, sentencia_set, condiciones_where):
        try:
            with self.connection.cursor() as cursor:
                consulta = f"UPDATE {tabla_from} SET {sentencia_set} WHERE {condiciones_where} "
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al modificar registro: {e}")
    
    def eliminarRegistro(self, tabla_from, condiciones_where, cantidad=0):
        try:
            with self.connection.cursor() as cursor:
                consulta = f"DELETE FROM {tabla_from} WHERE {condiciones_where} "
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al recuperar registros: {e}")
