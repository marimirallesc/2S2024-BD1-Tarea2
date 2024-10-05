document.addEventListener('DOMContentLoaded', function() {
    const userId = document.getElementById('userId').value;
    const empleadoId = document.getElementById('empleadoId').value;
    const empleadoVDI = document.getElementById('empleadoVDI').value;

    console.log(`Fetching movimientos for empleadoVDI: ${empleadoVDI}`);

    // Obtener la lista de movimientos del empleado
    fetch(`/listar_movimientos/${userId}/${empleadoId}`)
        .then(response => response.json())
        .then(result => {
            const tbody = document.getElementById('movimientosTableBody');
            tbody.innerHTML = '';  // Limpiar la tabla antes de agregar nuevos datos

            // Comprobar si la respuesta es exitosa
            if (result.success) {
                // Si hay movimientos, agregar cada movimiento a la tabla
                result.movimientos.forEach(movimiento => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${movimiento.Fecha}</td>
                        <td>${movimiento.TipoMovimiento}</td>
                        <td>${movimiento.Monto}</td>
                        <td>${movimiento.NuevoSaldo}</td>
                        <td>${movimiento.PostByUsuario}</td>
                        <td>${movimiento.PostInIp}</td>
                        <td>${movimiento.PostTime}</td>
                    `;
                    tbody.appendChild(row);
                });
            } else {
                // Si no hay movimientos, mostrar un mensaje
                alert('No hay movimientos.');
                //window.location.href = `/index/${userId}`; // Redirigir a la lista de empleados
            }
        })
        .catch(error => {
            console.error('Error fetching movimientos list:', error);
            alert('Error al obtener la lista de movimientos.');
        });
});
