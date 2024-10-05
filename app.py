from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from ConectarBD import MssqlConnection

app = Flask(__name__)

app.secret_key = '0000'

@app.route('/')
def login():
    return render_template('login.html')

# Esta funcion deberia llamarse login_usuario
# yo no lo cambie por si rompe lo demas
@app.route('/login_empleado', methods=['POST'])
def login_empleado():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        db = MssqlConnection()
        usuario = db.login(username, password)
        # Verificar si la consulta devolvió algún resultado
        if usuario[0][0] == 0:
            userId = usuario[0][1]
            return jsonify({'success': True, 'userId': userId})
        else:
            return jsonify({'success': False, 'message': db.descripcionError(usuario[0][0])}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/logout_empleado', methods=['POST'])
def logout_empleado():
    data = request.get_json()
    userId = data.get('userId')
    try:
        db = MssqlConnection()
        usuario = db.logout(userId)
        # Verificar si la consulta devolvió algún resultado
        if usuario == 0:
            return jsonify({'success': True, 'userId': userId})
        else:
            return jsonify({'success': False, 'message': db.descripcionError(usuario)}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/index/<int:userId>')
def index(userId):
    return render_template('index.html', userId=userId) 

@app.route('/listar_empleados/<int:userId>', methods=['GET'])
def listar_empleados(userId):
    try:
        db = MssqlConnection()
        empleados = db.listarEmpleados(userId)
        if empleados == 50008:  # Error en la BD
            raise Exception("Lista de empleados no disponible")
        return jsonify(empleados)
    except Exception as e:
        print(f"Error al listar empleados: {e}")
        return jsonify({'error': str(e)}), 500  # Devuelve un código de error adecuado
    
@app.route('/consultar/<int:userId>/<int:empleado_vdi>', methods=['GET'])
def consultar_empleado(userId, empleado_vdi):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_vdi))  # Busca el empleado por el VDI

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            return render_template('consultar.html', empleado=empleado[0], userId=userId)
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")
    
@app.route('/buscar/<int:userId>/<buscar>', methods=['GET'])
def buscar(userId, buscar):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(buscar))  # Busca el empleado por el ID

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            return render_template('consultar.html', empleado=empleado[0], userId=userId)
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")

@app.route('/insertar/<int:userId>', methods=['GET'])
def insertar(userId):
    db = MssqlConnection()
    puestos = db.listarPuestos()
    return render_template('insertar.html', userId=userId, puestos=puestos)

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
        else:
            return jsonify({'success': False, 'message': db.descripcionError(resultado)}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/editar/<int:userId>/<int:empleado_id>', methods=['GET'])
def editar_empleado(userId, empleado_id):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_id))  # Busca el empleado por el ValorDocumentoIdentidad
        puestos = db.listarPuestos()

        if empleado and len(empleado) > 0:
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
        
        resultado = db.editarEmpleado(userId, empleadoId, identificacion, nombre, puestoIndex)
        if resultado == 0:
            return jsonify({'success': True}) # Devuelve un objeto JSON en caso de éxito
        else:
            return jsonify({'success': False, 'message': db.descripcionError(resultado)}), 401

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
            return jsonify({'success': False, 'message': db.descripcionError(resultado)}), 401
    except Exception as e:
        print(f"Error al eliminar empleado: {e}")
        return jsonify({'message': 'Error en el servidor.'}), 500

@app.route('/movimientos/<int:userId>/<int:empleado_vdi>')
def movimientos(userId, empleado_vdi):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_vdi))  # Busca el empleado por el VDI

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            empleado_id = empleado[0]['Id']
            return render_template('movimientos.html', userId=userId, empleado_vdi=empleado_vdi, empleado=empleado[0], empleado_id=empleado_id) 
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")
    

@app.route('/listar_movimientos/<int:userId>/<int:empleado_id>', methods=['GET'])
def listar_movimientos(userId, empleado_id):
    try:
        db = MssqlConnection()
        userId = userId
        movimientos = db.listarMovimientos(empleado_id)
        
        # Si se encontraron movimientos, los retornamos
        if movimientos and len(movimientos) > 0:
            return jsonify({'success': True, 'movimientos': movimientos})
        else:
            # Si no hay movimientos, retornar success: false y un arreglo vacío
            return jsonify({'success': False, 'movimientos': []}), 200
    except Exception as e:
        print(f"Error al listar movimientos: {e}")
        return jsonify({'error': str(e)}), 500  # Devuelve un código de error adecuado

@app.route('/insert_movimiento/<int:userId>/<int:empleado_vdi>', methods=['GET'])
def insert_movimiento(userId, empleado_vdi):
    try:
        db = MssqlConnection()
        tipoMovimiento = db.listarTipoMovimientos()
        empleado = db.listarEmpleados(userId, buscar=str(empleado_vdi))  # Busca el empleado por el VDI

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            empleado_id = empleado[0]['Id']
            return render_template('insertar_movimiento.html', userId=userId, empleado=empleado[0], empleado_id=empleado_id, empleado_vdi=empleado_vdi, tipoMovimiento=tipoMovimiento)
        else:
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        return render_template('index.html', error="Error al obtener empleado")

@app.route('/insertar_movimiento', methods=['POST'])
def insertar_movimiento():
    try:
        data = request.json
        userId = data.get('userId')
        empleadoId = data.get('empleadoId')
        vdi = data.get('vdi')
        tipoMovimiento = data.get('tipoMovimiento')
        monto = data.get('monto')
        montoOriginal = data.get('montoOriginal')
        nuevoSaldo = data.get('nuevoSaldo')

        db = MssqlConnection()

        resultado = db.insertarMovimiento(userId, empleadoId, tipoMovimiento, montoOriginal)

        if resultado == 0:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': db.descripcionError(resultado)}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})




if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')
