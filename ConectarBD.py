import pyodbc

class MssqlConnection:
    def __init__(self):
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=mssql-181428-0.cloudclusters.net,19997;'
            'DATABASE=BD_SegundaTarea;'
            'UID=Usuario;'
            'PWD=Usuario1'
        )

    def connect_mssql(self):
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as ex:
            print(f"Connection error: {ex}")
            raise
    
    # Lista los empleados, recibe un parametro opcional
    # para buscar por nombre o identificacion
    def listarEmpleados(self, buscar = ""): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarEmpleados] @Buscar=?, @OutResult=0;", (buscar)) 
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            empleados = cursor.fetchall()        
            cursor.close()
            connect.close()
            print('Empleados: ', empleados)
            return [{'Id': row[0], 'Puesto': row[1], 'ValorDocumentoIdentidad': row[2]
                     , 'Nombre': row[3], 'FechaContratacion': row[4], 'SaldoVacaciones': row[5]} for row in empleados]
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return result    

    # Lista los movimientos de un empleado, recibe el id de un empleado
    def listarMovimientos(self, id): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarMovimientos] @IdEmpleado=?, @OutResult=0;", (id))
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            movimientos = cursor.fetchall()        
            cursor.close()
            connect.close()
            print('Movimientos: ', movimientos)
            return [{'Fecha': row[0], 'TipoMovimiento': row[1], 'Monto': row[2]
                     , 'NuevoSaldo': row[3], 'PostByUsuario': row[4]
                     , 'PostInIp': row[5], 'PostTime': row[6]} for row in movimientos]
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return result    

    # Retorna la descripcion del error, recibe el codigo de un error
    def descripcionError(self, codigo): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[DescripcionError] @Codigo=?, @OutResult=0;", (codigo)) 
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            descripcionError = cursor.fetchall()[0][0]        
            cursor.close()
            connect.close()
            print(descripcionError)
            return descripcionError
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return 'Error en la base de datos ' + result   

    # Login, recibe el nombre de usuario y contrase�a
    def login(self, username, password): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[Login] @Username=?, @Password=?, @OutResult=0;"
                       , (username, password))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result
        # Retorna 0 si el usuario y contrase�a son correctos
        # 50001 Si el usuario no existe
        # 50002 si la contrase�a es incorrecta


    # def insertarEmpleado(self, nombre, salario):
    #     try:
    #         connect = self.connect_mssql()
    #         cursor = connect.cursor()
    #         cursor.execute("""
    #             EXECUTE [dbo].[InsertarEmpleado] @inNombre=?, @inSalario=?, @OutResult=0;
    #             """, (nombre, salario))
    #         resultado = cursor.fetchall()[0][0]
    #         connect.commit()
    #         cursor.close()
    #         connect.close()
    #         # Retorna 0 si todo fue exitoso o 50006 si el Empleado ya existe
    #         return  resultado
    #     except pyodbc.Error as ex:
    #         print(f"Error inserting employee: {ex}")
    #         return -1  # Retorna -1 si hubo un error

if __name__ == '__main__':
    # Ejemplo de uso
    x = MssqlConnection()
    nombre = '1'

    #x.listarEmpleados(nombre)
    #x.listarMovimientos(nombre)
    #x.descripcionError(50007)
    x.login('UsuarioScripts', 'UsuarioScripts')
    #x.login('mgarrison', 'sdv')
    
