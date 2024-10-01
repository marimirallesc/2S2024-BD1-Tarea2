from tkinter import NO
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
    
    # Lista los empleados, recibe el id del usuario
    # y un parametro opcional para buscar por nombre o identificacion
    def listarEmpleados(self, userId, buscar = ""): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarEmpleados] @UserId=?, @Buscar=?, @OutResult=0;"
                       , (userId, buscar)) 
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            empleados = cursor.fetchall()   
            connect.commit()
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
        
    # Lista los puestos
    def listarPuestos(self): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarPuestos] @OutResult=0;")
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            puestos = cursor.fetchall()        
            cursor.close()
            connect.close()
            print('Puestos: ', puestos)
            return [{'Id': row[0], 'Nombre': row[1], 'SalarioxHora': row[2]} for row in puestos]
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return result  

    # Lista los tipos de movimientos
    def listarTipoMovimientos(self): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarTipoMovimientos] @OutResult=0;")
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            movimientos = cursor.fetchall()        
            cursor.close()
            connect.close()
            print('Tipo de movimientos: ', movimientos)
            return [{'Id': row[0], 'Nombre': row[1], 'TipoAccion': row[2]} for row in movimientos]
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
        result = cursor.fetchall()
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result
        # Login exitoso: return [(0, IdUsuario)]
        # Si el usuario no existe: [(50001,)] 
        # Si la contrase�a es incorrecta: [(50002,)]
        # Login desabilitado: [(50003,)]

    # Logout, recibe el id del usuario
    def logout(self, userId): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[Logout] @UserId=?, @OutResult=0;"
                       , (userId))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # EliminarEmpleado, recibe el id del usuario y del empleado
    def eliminarEmpleado(self, userId, empleadoId): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[EliminarEmpleado] @UserId=?, @EmpleadoId=?, @OutResult=0;"
                       , (userId, empleadoId))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # IntentoEliminarEmpleado, recibe el id del usuario y del empleado
    def intentoEliminarEmpleado(self, userId, empleadoId): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[IntentoEliminarEmpleado] @UserId=?, @EmpleadoId=?, @OutResult=0;"
                       , (userId, empleadoId))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result


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
    nombre = 'a'

    x.intentoEliminarEmpleado(1, 1)
    #x.eliminarEmpleado(1, 12)
    #x.listarEmpleados(1)
    #x.listarEmpleados(1, nombre)
    #x.listarMovimientos(1)
    #x.listarPuestos()
    #x.listarTipoMovimientos()
    #x.descripcionError(50007)
    #x.login('UsuarioScripts', 'UsuarioScripts')
    #x.login('mgarrison', 'sdv')
    #x.logout(1)
    
