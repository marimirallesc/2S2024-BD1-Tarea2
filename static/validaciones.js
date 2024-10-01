
function validaciones() {
    const nombreInput = document.getElementById('nombre');
    const salarioInput = document.getElementById('salario');

    let valid = true;

    // Validar el nombre (solo caracteres alfabéticos y espacios)
    const nombreRegex = /^[A-Za-z\s-]+$/;
    if (!nombreRegex.test(nombreInput.value)) {
        alert('El nombre solo puede contener caracteres alfabéticos, espacios o guiones.');
        valid = false;
    }
    // Validar el salario (valor monetario válido)
    const salarioRegex = /^\d+(\.\d{1,2})?$/;
    if (!salarioRegex.test(salarioInput.value)) {
        alert('El salario debe ser un valor numérico válido.');
        valid = false;
    }
    return valid;
}
