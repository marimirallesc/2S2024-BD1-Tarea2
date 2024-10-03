document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('insertForm');
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Previene el envío normal del formulario
        
        try {
            const valid = validaciones();   // Realizar validaciones 
            if (!valid) {   
                console.log('Error datos de entrada incorrectos');
                return;     // Si las validaciones fallan, detener la ejecucion
            }

            const user = 1; //document.getElementById('userId').value;
            const nombre = document.getElementById('nombre').value;
            const puesto = document.getElementById('puesto').value;
            const vdi = document.getElementById('empleadoId').value;

            const response = await fetch('/insertar_empleado', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user, nombre, puesto, vdi })
            });

            const result = await response.json();

            if (result.success) {
                alert('Empleado insertado exitosamente.');
                window.location.href = '/'; // Redirigir a la lista de empleados
            } else {
                alert('Error al insertar el empleado: ' + result.message);
            }
        } catch (error) {
            console.error('Error al insertar empleado:', error);
            alert('Hubo un error al insertar el empleado.');
        }
    });
});
