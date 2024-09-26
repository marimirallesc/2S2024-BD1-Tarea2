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
      
    # def listarEmpleados(self): 
    #     connect = self.connect_mssql()
    #     cursor = connect.cursor()       
    #     cursor.execute("EXECUTE [dbo].[ListarEmpleados] 0")    
    #     if cursor.fetchall()[0][0] == 0: 
    #         cursor.nextset()
    #         empleados = cursor.fetchall()        
    #         cursor.close()
    #         connect.close()
    #         #print('Empleados: ', empleados)
    #         return [{'Id': row[0], 'Nombre': row[1], 'Salario': float(row[2])} for row in empleados]
    #     else:   # Error en la BD
    #         cursor.close()
    #         connect.close()
    #         return 50005    

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

    #conexion = MssqlConnection()

    #nombre = 'Pepe Cruz'
    #salario = 500000
    #conexion.insertarEmpleado(nombre, salario)
    #empleados = conexion.listarEmpleados()
    MssqlConnection().listarEmpleados()
