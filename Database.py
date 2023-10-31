'''Módulo para establecer conexiones con SQL'''

import mysql.connector


class Config:
    '''Configurar conexion'''

    def connect(self):
        '''Conectar a la base de datos'''
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port='3306'
        )

    def close(self):
        '''Cerrar la base de datos'''
        self.connection.close()

    def imprimirTablas(self):
        '''Mostrar tablas de la base'''
        cursor = self.connection.cursor()
        use = 'USE MetaClr'
        cursor.execute(use)
        sql = 'SELECT ID_Alimento, Alimento FROM alimentos LIMIT 10'
        cursor.execute(sql)
        return cursor.fetchall()

        # self.connection.commit()

    # Base de datos de usuarios


class UserDatabase(Config):
    '''Base de datos del usuario'''

    def __init__(self, route) -> None:
        super().__init__()
        self.route = route

    def registrarUsuario(self, datos):
        '''Registrar nuevo usuario'''
        use = 'USE MetaClr'
        camposTabla = 'Nombre,nickname,contrasenia'
        qntd = '%s, %s, %s'
        sql = f'INSERT INTO Usuario({camposTabla}) VALUES ({qntd})'
        cursor = self.connection.cursor()
        cursor.execute(use)
        cursor.execute(sql, datos)
        self.connection.commit()
        return 'introducido'

    def verificarLogin(self, datos):
        '''Buscar por un usuario existente'''
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
