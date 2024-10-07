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
    def listarEmpleados(self, idUsuario, buscar = ""): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarEmpleados] @idUsuario=?, @Buscar=?, @OutResult=0;"
                       , (idUsuario, buscar)) 
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            empleados = cursor.fetchall()   
            connect.commit()
            cursor.close()
            connect.close()
            print('Empleados: ', empleados)
            return [{'Id': row[0], 'Puesto': row[1], 'ValorDocumentoIdentidad': row[2]
                     , 'Nombre': row[3], 'FechaContratacion': row[4].strftime("%d-%m-%Y"), 'SaldoVacaciones': row[5]} for row in empleados]
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return result    

    # Obtiene los detalles de un empleado, recibe el ValorDocumentoIdentidad
    def consultarEmpleado(self, userId, buscar = ""): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ConsultarEmpleado] @Buscar=?, @OutResult=0;"
                       , (buscar)) 
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            empleados = cursor.fetchall()   
            connect.commit()
            cursor.close()
            connect.close()
            print('Empleados: ', empleados)
            return [{'Id': row[0], 'Puesto': row[1], 'ValorDocumentoIdentidad': row[2]
                     , 'Nombre': row[3], 'FechaContratacion': row[4].strftime("%d-%m-%Y"), 'SaldoVacaciones': row[5]} for row in empleados]
        else:   # Error en la BD
            cursor.close()
            connect.close()
            return result    

    # Lista los movimientos de un empleado, recibe el id de un empleado
    def listarMovimientos(self, idEmpleado): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[ListarMovimientos] @idEmpleado=?, @OutResult=0;", (idEmpleado))
        result = cursor.fetchall()[0][0]
        if result == 0: 
            cursor.nextset()
            movimientos = cursor.fetchall()        
            cursor.close()
            connect.close()
            print('Movimientos: ', movimientos)
            return [{'Fecha': row[0].strftime("%d-%m-%Y"), 'TipoMovimiento': row[1], 'Monto': int(round(row[2]))
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

    # Login, recibe el nombre de usuario y contrasena
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
        # Si la contrasena es incorrecta: [(50002,)]
        # Login desabilitado: [(50003,)]

    # Logout, recibe el id del usuario
    def logout(self, idUsuario): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[Logout] @idUsuario=?, @OutResult=0;"
                       , (idUsuario))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # EliminarEmpleado, recibe el id del usuario y del empleado
    def eliminarEmpleado(self, idUsuario, idEmpleado): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[EliminarEmpleado] @idUsuario=?, @idEmpleado=?, @OutResult=0;"
                       , (idUsuario, idEmpleado))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # IntentoEliminarEmpleado, recibe el id del usuario y del empleado
    def intentoEliminarEmpleado(self, idUsuario, idEmpleado): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[IntentoEliminarEmpleado] @idUsuario=?, @idEmpleado=?, @OutResult=0;"
                       , (idUsuario, idEmpleado))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # InsertarEmpleado, recibe el id del usuario y identificacion, nombre y id del puesto del empleado
    def insertarEmpleado(self, idUsuario, identificacion, nombre, idPuesto): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[InsertarEmpleado] @idUsuario=?, @Identificacion=?, @Nombre=?, @idPuesto=?, @OutResult=0;"
                       , (idUsuario, identificacion, nombre, idPuesto))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # EditarEmpleado, recibe el id del usuario y id, identificacion, nombre y id del puesto del empleado
    def editarEmpleado(self, idUsuario, idEmpleado, identificacion, nombre, idPuesto): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[EditarEmpleado] @idUsuario=?, @idEmpleado=?, @NewIdentificacion=?, @NewNombre=?, @NewidPuesto=?, @OutResult=0;"
                       , (idUsuario, idEmpleado, identificacion, nombre, idPuesto))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result

    # InsertarMovimiento, recibe el id del usuario y identificacion, nombre y id del puesto del empleado
    def insertarMovimiento(self, idUsuario, idEmpleado, idTipoMovimiento, monto): 
        connect = self.connect_mssql()
        cursor = connect.cursor()       
        cursor.execute("EXECUTE [dbo].[InsertarMovimiento] @idUsuario=?, @idEmpleado=?, @idTipoMovimiento=?, @monto=?, @OutResult=0;"
                       , (idUsuario, idEmpleado, idTipoMovimiento, monto))    
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        connect.close()
        print(result)
        return result


if __name__ == '__main__':
    # Ejemplo de uso
    x = MssqlConnection()
    nombre = 'vcvc'

    #x.insertarMovimiento(1, 1, 5, 5)
    #x.editarEmpleado(1, 4, '896', 'Jensen', 6 )
    #x.insertarEmpleado(1, '2433', 'Alan', 2 )
    #x.intentoEliminarEmpleado(1, 2)
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
    
