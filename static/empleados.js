document.addEventListener('DOMContentLoaded', function() {
    // Verifica si hay un mensaje de error
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        alert(errorMessage.value);  // Muestra la alerta con el mensaje de error
        window.location.href = '/';  // Redirige al index.html
    }

    fetch('/listar_empleados')
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
                        <button onclick="window.location.href='/consultar/${empleado.ValorDocumentoIdentidad}'">Consultar</button>
                        <br></br>            
                        <button onclick="window.location.href='/editar/${empleado.Id}'">Editar</button>
                        <button onclick="eliminarEmpleado(${empleado.Id}, '${empleado.Nombre}', '${empleado.ValorDocumentoIdentidad}')">Eliminar</button>
                    </td>
                `;

                tbody.appendChild(row);
            });
        })
        .catch(error => {
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
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload();  // Recargar la página para actualizar la lista
            } else {
                alert('Error al eliminar el empleado');
            }
        })
        .catch(error => {
            console.error('Error al eliminar el empleado:', error);
        });
    }
}

