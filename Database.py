import mysql.connector
from datetime import datetime

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
        camposTabla = ('Nombre,nickname,contrasenia,TMB,Edad,Altura,Peso,Sexo')
        qntd = ('%s, %s, %s, %s, %s, %s, %s, %s')
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
        
    def obtenerTMB(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT TMB
        FROM Usuario
        WHERE ID_Usuario = %s'''
        cursor.execute(sql, (id,))
        return cursor.fetchone()
        
    def ObtenerRegistros(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT A.Alimento,RA.Total_Calorias,RA.Horario,RA.Total_proteinas,RA.Total_lipidos,RA.Total_hidratos,RA.Fecha_Registro,RA.ID_RegistroAlimento
        FROM Registro_Alimentos AS RA
        JOIN Alimentos AS A ON A.ID_Alimento = RA.ID_Alimento
        WHERE RA.ID_Usuario = %s ORDER BY RA.Fecha_Registro DESC'''
        cursor.execute(sql, (id,))
        return cursor.fetchall()
    
    def obtenerRegistrosSemana(self, id, fecha):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        fecha_formateada = fecha.strftime('%Y-%m-%d')
        sql = '''
        SELECT Total_Calorias, Total_lipidos, Total_Proteinas, Total_hidratos
        FROM Registro_Alimentos
        WHERE Fecha_Registro BETWEEN STR_TO_DATE(%s, '%Y-%m-%d') - INTERVAL ((DAYOFWEEK(STR_TO_DATE(%s, '%Y-%m-%d')) + 5) % 7) DAY AND STR_TO_DATE(%s, '%Y-%m-%d') AND ID_Usuario = %s
        '''
        cursor.execute(sql, (fecha_formateada,fecha_formateada,fecha_formateada,id,))
        return cursor.fetchall()
    
    def eliminarRegistroAlimento(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''DELETE FROM Registro_Alimentos
        WHERE ID_RegistroAlimento = %s
        '''
        cursor.execute(sql,(id,))
        self.connection.commit()
        return 'Eliminado'
        
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
        print(f"INSERT INTO {tabla_from} {valores_insertados} VALUES {condiciones_where}")
        try:
            with self.connection.cursor() as cursor:
                consulta = f"INSERT INTO {tabla_from} {valores_insertados} VALUES {condiciones_where}"
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al insertar registro/s: {e}")

        return not None
    
    def modificarRegistro(self, tabla_from, sentencia_set, condiciones_where):
        try:
            with self.connection.cursor() as cursor:
                consulta = f"UPDATE {tabla_from} SET {sentencia_set} WHERE {condiciones_where} "
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al modificar registro: {e}")
            return None

        return not None
    
    def eliminarRegistro(self, tabla_from, condiciones_where):
        print(f"DELETE FROM {tabla_from} WHERE {condiciones_where} ")
        try:
            with self.connection.cursor() as cursor:
                consulta = f"DELETE FROM {tabla_from} WHERE {condiciones_where} "
                cursor.execute(consulta)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error al recuperar registros: {e}")
            return None

        return not None
