document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('editForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Previene el envío normal del formulario

        try {
            const valid = validaciones();   // Realizar validaciones 
            if (!valid) {   
                console.log('Error datos de entrada incorrectos');
                return;     // Si las validaciones fallan, detener la ejecucion
            }

            const user = document.getElementById('userId').value;
            const empleadoId = document.getElementById('empleadoId').value;
            const nombre = document.getElementById('nombre').value;
            const puesto = document.getElementById('puesto').value;
            const identificacion = document.getElementById('identificacion').value;

            // Validar los datos del formulario antes de enviarlos
            if (!validateEditForm(nombre, puesto)) {
                console.log('Error: datos de entrada incorrectos');
                return; // Si la validación falla, detener el proceso
            }

            // Imprimir los datos que se están enviando
            //console.log('Datos enviados:', { user, empleadoId, identificacion , nombre, puesto});

            const response = await fetch(`/actualizar_empleado`, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user, empleadoId, nombre, puesto, identificacion })
            });


            if (!response.ok) {
                const errorText = await response.text(); // Ver el texto de la respuesta del servidor en caso de error
                console.error('Error en la respuesta del servidor:', errorText);
                alert('Error al actualizar el empleado: ' + errorText);
                return;
            }

            const result = await response.json();

            if (result.success) {
                alert('Empleado actualizado exitosamente.');
                window.location.href = `/index/${user}`; // Redirigir a la lista de empleados
            } else {
                alert('Error al actualizar el empleado: ' + result.message);
            }
        } catch (error) {
            console.error('Error capturado en el catch:', error);
            alert('El empleado no fue actualizado.');
        }
    });

    // Función de validación del formulario de edición
    function validateEditForm(nombre, puesto) {
        if (!nombre || !puesto) {
            alert('Todos los campos son obligatorios.');
            return false;
        }
        return true;
    }
});
