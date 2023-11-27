import mysql.connector
import datetime

class Config:
    def connect(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            port = '3306'
        )
    # def connect(self):
    #     self.connection = mysql.connector.connect(
    #         host = '137.184.234.157',
    #         user = 'metaclrlng23',
    #         password = 'Clr23BX',
    #         database = 'metaclr',
    #         port = '3306'
    #     )
        
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
        sql_usuario = f'INSERT INTO Usuario({camposTabla}) VALUES ({qntd})'
        sql_insert_usuario_metas = 'INSERT INTO Usuario_Metas(ID_Usuario, ID_Meta, Fecha_Establecimiento, Progreso) VALUES (%s, %s, %s, %s)'

        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql_usuario,datos)
        self.connection.commit()

        # ultimo_id_usuario = cursor.lastrowid
        # fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
        # metas_a_insertar = [
        #     {'ID_Meta': 4, 'Progreso': 0.0},
        #     {'ID_Meta': 5, 'Progreso': 0.0}
        # ]
        # for meta in metas_a_insertar:
        #     cursor.execute(sql_insert_usuario_metas, (ultimo_id_usuario, meta['ID_Meta'], fecha_actual, meta['Progreso']))
        #     self.connection.commit()
        return not None
    
    def datosUsuario(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT ObjetivosCumplidos
        FROM Usuario
        WHERE ID_Usuario = %s'''
        cursor.execute(sql, (id,))
        return cursor.fetchone()
    
    def verificarLogin(self,datos):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        consulta = " SELECT Nickname, contrasenia,ID_Usuario,Nombre FROM Usuario WHERE Nickname = %s AND contrasenia = %s"
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
        sql = '''SELECT A.Alimento,RA.Total_Calorias,RA.Horario,RA.Total_proteinas,RA.Total_lipidos,RA.Total_hidratos,RA.Fecha_Registro,RA.ID_RegistroAlimento,A.Categoria
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

class MetaDatabase(Config):
    def __init__(self,route) -> None:
        super().__init__()
        
        self.route = route
        
    def verificarMeta(self, fecha,id,tipo):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT DATE(UM.Fecha_Establecimiento)
        FROM Usuario_Metas AS UM
        JOIN Metas AS M ON M.ID_Meta = UM.ID_Meta
        WHERE DATE(UM.Fecha_Establecimiento) = %s AND UM.ID_Usuario = %s AND M.Tipo_Meta = %s'''
        cursor.execute(sql, (fecha,id,tipo,))
        return cursor.fetchall()
    
    def verificarMetaSemanal(self, fecha,id,tipo):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT *
        FROM Usuario_Metas AS UM
        JOIN Metas AS M ON M.ID_Meta = UM.ID_Meta
        WHERE WEEK(UM.Fecha_Establecimiento) = %s AND UM.ID_Usuario = %s AND M.Tipo_Meta = %s'''
        cursor.execute(sql, (fecha,id,tipo,))
        return cursor.fetchall()
    
    def obtenerMetasEnProgreso(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT UM.ID_Relacion, UM.Progreso, U.Valor_Predeterminado, U.Tipo_Meta,U.Tipo,U.ID_Meta
        FROM Usuario_Metas UM
        JOIN Metas U ON U.ID_Meta = UM.ID_Meta
        WHERE UM.ID_Usuario = %s'''
        cursor.execute(sql, (id,))
        return cursor.fetchall()
    
    def actualizarObjetivosUsuario(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql_update_usuario = '''UPDATE Usuario
        SET ObjetivosCumplidos = ObjetivosCumplidos + 1
        WHERE ID_Usuario = %s
        '''
        cursor.execute(sql_update_usuario,(id,))
        self.connection.commit()
        
    def restarObjetivosUsuario(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql_update_usuario = '''UPDATE Usuario
        SET ObjetivosCumplidos = ObjetivosCumplidos - 1
        WHERE ID_Usuario = %s
        '''
        cursor.execute(sql_update_usuario,(id,))
        self.connection.commit()
    
    def registrarProgresoMeta(self,id,nuevoProgreso,estado,idMeta):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''UPDATE Usuario_Metas
        SET Progreso = %s, Estado = %s
        WHERE ID_Usuario = %s AND ID_Meta = %s;
        '''
        cursor.execute(sql,(nuevoProgreso,estado,id,idMeta))
        self.connection.commit()
        
    def registraMeta(self,datos):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        camposTabla = ('ID_Usuario,ID_Meta,Fecha_Establecimiento,Progreso')
        qntd = ('%s, %s, %s, %s')
        sql = f'INSERT INTO Usuario_Metas({camposTabla}) VALUES ({qntd})'
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql,datos)
        self.connection.commit()
    
    def obtenerMeta(self,id):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT M.Valor_Predeterminado,M.Descripcion,UM.Progreso,U.ObjetivosCumplidos
        FROM Metas M
        JOIN Usuario_Metas UM ON M.ID_Meta = UM.ID_Meta
        JOIN Usuario U ON UM.ID_Usuario = U.ID_Usuario
        WHERE U.ID_Usuario = %s;
        '''
        cursor.execute(sql, (id,))
        return cursor.fetchall()
    
    def obtenerRegistrosSem(self,id,tipo,fecha):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT UM.Progreso, UM.Estado
        FROM Usuario_Metas AS UM
        JOIN Metas AS M ON M.ID_Meta = UM.ID_Meta
        WHERE UM.ID_Usuario = %s AND M.Tipo = %s AND WEEK(UM.Fecha_Establecimiento) = %s;
        '''
        cursor.execute(sql, (id,tipo,fecha))
        return cursor.fetchall()
    
    def obtenerRegistrosDiarios(self,id,idMeta,fecha):
        cursor = self.connection.cursor()
        use = 'USE metaclr'
        cursor.execute(use)
        sql = '''SELECT UM.Progreso, UM.Estado
        FROM Usuario_Metas AS UM
        JOIN Metas AS M ON M.ID_Meta = UM.ID_Meta
        WHERE UM.ID_Usuario = %s AND UM.ID_Meta = %s AND DATE(UM.Fecha_Establecimiento) = %s;
        '''
        cursor.execute(sql, (id,idMeta,fecha))
        return cursor.fetchone()