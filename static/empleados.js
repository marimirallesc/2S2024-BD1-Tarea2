document.addEventListener('DOMContentLoaded', function() {
    // Verifica si hay un mensaje de error
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        alert(errorMessage.value);  // Muestra la alerta con el mensaje de error
        window.location.href = '/';  // Redirige al index.html
    }
    const userId = document.getElementById('userId').value;
    console.log(`Fetching empleados for userId: ${userId}`);
    fetch(`/listar_empleados/${userId}`)
        .then(response => response.json())
        .then(empleados => {
            const tbody = document.getElementById('employeeTableBody');
            tbody.innerHTML = '';  // Limpiar la tabla antes de agregar nuevos datos

            empleados.forEach(empleado => {
                const row = document.createElement('tr');
                
                row.innerHTML = `
                    <td>${empleado.ValorDocumentoIdentidad}</td>
                    <td>${empleado.Nombre}</td>
                    <td>${empleado.Puesto}</td>
                    <td>${empleado.FechaContratacion}</td>
                    <td>${empleado.SaldoVacaciones}</td>
                    <td>
                        <button onclick="window.location.href='/consultar/${userId}/${empleado.ValorDocumentoIdentidad}'">Consultar</button>
                        <br></br>            
                        <button onclick="window.location.href='/editar/${userId}/${empleado.ValorDocumentoIdentidad}'">Editar</button>
                        <button onclick="eliminarEmpleado(${empleado.Id}, '${empleado.Nombre}', '${empleado.ValorDocumentoIdentidad}')">Eliminar</button>
                    </td>
                `;

                tbody.appendChild(row);
            });
        })
        .catch(error => {
            //alert('Error fetching employee list.');
            console.error('Error fetching employee list:', error);
        });
});

// Función para eliminar empleado
function eliminarEmpleado(id, nombre, documento) {
    const confirmDelete = confirm(`¿Está seguro de eliminar el empleado ${nombre} con Documento de Identidad ${documento}?`);
    if (confirmDelete) {
        fetch(`/eliminar/${id}`, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            location.reload();  // Recargar la página para actualizar la lista
        })
        .catch(error => {
            alert('Error al eliminar el empleado: ' + error.message);
            console.error('Error al eliminar el empleado:', error);
        });
    }
}

