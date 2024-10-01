// Función para enviar el formulario de edición de empleado
function submitEditForm() {
    const id = document.getElementById('empleadoId').value;
    const nombre = document.getElementById('nombre').value;
    const salario = document.getElementById('salario').value;
    const puesto = document.getElementById('puesto').value;

    // Validar los datos del formulario
    if (validateEditForm(nombre, salario, puesto)) {
        const data = {
            nombre: nombre,
            salario: parseFloat(salario),
            puesto: puesto
        };

        fetch(`/empleados/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            } else {
                alert('Error al actualizar el empleado.');
            }
        })
        .catch(error => console.error('Error al actualizar empleado:', error));
    }
}

// Manejar el envío del formulario de edición
document.getElementById('editForm').addEventListener('submit', function(event) {
    event.preventDefault();
    submitEditForm();
});
