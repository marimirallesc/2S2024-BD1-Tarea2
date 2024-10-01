document.addEventListener('DOMContentLoaded', function() {
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
                        <button onclick="window.location.href='/consultar'">Consultar</button>
                        <br>
                        <button onclick="window.location.href='/editar'">Editar</button>
                        <button onclick="">Eliminar</button>
                    </td>
                `;

                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching employee list:', error);
        });
});
