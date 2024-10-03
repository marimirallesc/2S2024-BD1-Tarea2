from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from ConectarBD import MssqlConnection

app = Flask(__name__)

app.secret_key = '0000'

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/insertar/')
def insertar():
    return render_template('insertar.html')

@app.route('/editar/')
def editar():
    # Pasar un empleado ficticio para evitar el error
    empleado = {
        'Nombre': '',
        'IdPuesto': 1
    }

    # Pasar también una lista ficticia de puestos
    puestos = [
        {'id': 1, 'nombre': 'Gerente'},
        {'id': 2, 'nombre': 'Asistente'},
        {'id': 3, 'nombre': 'Desarrollador'}
    ]

    return render_template('editar.html', empleado=empleado, puestos=puestos)
    
@app.route('/consultar/<int:id>', methods=['GET'])
def consultar_empleado(id):
    try:
        db = MssqlConnection()
        empleado = db.listarEmpleados(buscar=str(id))  # Busca el empleado por el ID

        # Verificar si se obtuvo un resultado válido
        if empleado and len(empleado) > 0:
            # Si se encuentra el empleado, renderiza la página de consulta
            return render_template('consultar.html', empleado=empleado[0])
        else:
            # Si no se encuentra el empleado, redirigir al index con un mensaje de error
            return render_template('index.html', error="Empleado no encontrado")
    except Exception as e:
        print(f"Error al obtener empleado: {e}")
        # Si ocurre un error inesperado, redirigir al index con un mensaje de error
        return render_template('index.html', error="Error al obtener empleado")


# Rutas existentes
@app.route('/listar_empleados', methods=['GET'])
def listar_empleados():
    try:
        userid=1
        db = MssqlConnection()
        empleados = db.listarEmpleados(userid)
        if empleados == 50005:  #Error en la BD
            raise Exception("Lista de empleados no disponible")
        else:
            return jsonify(empleados)
    except Exception as e:
        print(f"Error al listar empleados: {e}")  # Agrega un mensaje de error para depuración
        return jsonify({'error': str(e)})
    

@app.route('/insertar_empleado', methods=['POST'])
def insertar_empleado():
    try:
        data = request.json
        nombre = data.get('nombre')
        salario = data.get('salario')
        
        db = MssqlConnection()
        resultado = db.insertarEmpleado(nombre, salario)
        
        if resultado == 0:
            return jsonify({'success': True})
        elif resultado == 50006:
            return jsonify({'success': False, 'message': 'El empleado ya existe'})
        else:
            return jsonify({'success': False, 'message': 'Error al insertar el empleado'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')
