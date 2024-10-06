document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('insertMovimientoForm');
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Previene el envío normal del formulario
        
        const userId = document.getElementById('userId').value;
        const empleadoId = document.getElementById('empleadoId').value;
        const vdi = document.getElementById('vdi').value;
        const tipoMovimiento = document.getElementById('tipoMovimiento').value;
        const monto = parseFloat(document.getElementById('monto').value);

        try {
            const response = await fetch('/insert_movimiento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userId, empleadoId, tipoMovimiento, monto })
            });

            const result = await response.json();

            if (result.success) {
                alert('Movimiento insertado exitosamente.');
                window.location.href = `/movimientos/${userId}/${vdi}`; // Redirigir a la lista de movimientos
            } else {
                console.error(result.error + ': ' + result.message);
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error al insertar movimiento:', error);
            //alert('Hubo un error al insertar el movimiento.');
        }
    });
});
