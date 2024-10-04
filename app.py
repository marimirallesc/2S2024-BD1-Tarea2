from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from ConectarBD import MssqlConnection

app = Flask(__name__)

app.secret_key = '0000'

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    userId = 1;
    return render_template('index.html', userId=userId) 

@app.route('/insertar/<int:userId>')
def insertar(userId):
    db = MssqlConnection()
    puestos = db.listarPuestos()
    return render_template('insertar.html', userId=userId, puestos=puestos)

@app.route('/listar_empleados/<int:userId>', methods=['GET'])
def listar_empleados(userId):
    try:
        db = MssqlConnection()
        empleados = db.listarEmpleados(userId)
        if empleados == 50005:  # Error en la BD
            raise Exception("Lista de empleados no disponible")
        return jsonify(empleados)
    except Exception as e:
        print(f"Error al listar empleados: {e}")
        return jsonify({'error': str(e)}), 500  # Devuelve un código de error adecuado

@app.route('/insertar_empleado', methods=['POST'])
def insertar_empleado():
    try:
        data = request.json
        user = data.get('user')
        nombre = data.get('nombre')
        puesto = data.get('puesto')
        vdi = data.get('vdi')
        
        db = MssqlConnection()
        resultado = db.insertarEmpleado(user, vdi, nombre, puesto)
        
        if resultado == 0:
            return jsonify({'success': True})
        elif resultado == 50006:
            return jsonify({'success': False, 'message': 'El empleado ya existe'})
        else:
            return jsonify({'success': False, 'message': 'Error al insertar el empleado'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/consultar/<int:userId>/<int:empleado_id>', methods=['GET'])
def consultar_empleado(userId, empleado_id):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_id))  # Busca el empleado por el ID

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            return render_template('consultar.html', empleado=empleado[0])
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")


@app.route('/editar/<int:userId>/<int:empleado_id>', methods=['GET'])
def editar_empleado(userId, empleado_id):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_id))  # Busca el empleado por el ValorDocumentoIdentidad
        puestos = db.listarPuestos()

        if empleado and len(empleado) > 0:
            puestos_lista = [
                {'Id': 1, 'Nombre': 'Cajero'},
                {'Id': 2, 'Nombre': 'Camarero'},
                {'Id': 3, 'Nombre': 'Cuidador'},
                {'Id': 4, 'Nombre': 'Conductor'},
                {'Id': 5, 'Nombre': 'Asistente'},
                {'Id': 6, 'Nombre': 'Recepcionista'},
                {'Id': 7, 'Nombre': 'Fontanero'},
                {'Id': 8, 'Nombre': 'Niñera'},
                {'Id': 9, 'Nombre': 'Conserje'},
                {'Id': 10, 'Nombre': 'Albañil'}
            ]
            return render_template('editar.html', empleado=empleado[0], puestos=puestos, userId=userId)
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")

@app.route('/actualizar_empleado/', methods=['POST'])
def actualizar_empleado():
    try:
        data = request.get_json()  # Obtener los datos JSON del cuerpo de la solicitud
        userId = data['user']       # Acceder a los datos correctamente
        empleadoId = data['empleadoId']
        nombre = data['nombre']
        puestoIndex = data['puesto']
        identificacion = data['identificacion']

        db = MssqlConnection()
        
        db.editarEmpleado(userId, empleadoId, identificacion, nombre, puestoIndex)
        
        return {'success': True}  # Devuelve un objeto JSON en caso de éxito
    except Exception as e:
        print(f"Error al actualizar empleado: {e}")
        return {'success': False, 'message': "Error al actualizar empleado"}, 500  # Devuelve un error

@app.route('/eliminar/<int:empleado_id>', methods=['POST'])
def eliminar_empleado(empleado_id):
    try:
        # Supongamos que el UserId es 1, ajusta según tu lógica de usuarios.
        userId = 1
        db = MssqlConnection()
        
        # Llamar al método para eliminar el empleado
        resultado = db.eliminarEmpleado(userId, empleado_id)

        # Verifica si la eliminación fue exitosa
        if resultado == 0:
            return jsonify({'message': 'Empleado eliminado exitosamente.'})
        else:
            return jsonify({'message': 'Error al eliminar el empleado.'}), 400
    except Exception as e:
        print(f"Error al eliminar empleado: {e}")
        return jsonify({'message': 'Error en el servidor.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
