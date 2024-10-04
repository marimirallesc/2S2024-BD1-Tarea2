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

            const user = document.getElementById('userId').value;
            const nombre = document.getElementById('nombre').value;
            const puesto = document.getElementById('puesto').value;
            const identificacion = document.getElementById('identificacion').value;

            // Imprimir los datos que se están enviando
            //console.log('Datos enviados:', {user, identificacion , nombre, puesto});

            const response = await fetch('/insertar_empleado', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({user, identificacion , nombre, puesto})
            });

            const result = await response.json();

            if (result.success) {
                alert('Empleado insertado exitosamente.');
                window.location.href = `/index/${user}`; // Redirigir a la lista de empleados
            } else {
                alert('Error al insertar el empleado: ' + result.message);
            }
        } catch (error) {
            console.error('Error al insertar empleado:', error);
            alert('Hubo un error al insertar el empleado.');
        }
    });
});
