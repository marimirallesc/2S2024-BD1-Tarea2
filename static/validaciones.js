
function validaciones() {
    const nombreInput = document.getElementById('nombre');
    const identificacionInput = document.getElementById('vdi');

    let valid = true;

    // Validar el nombre (solo caracteres alfabéticos y espacios)
    const nombreRegex = /^[A-Za-z\s-]+$/;
    if (!nombreRegex.test(nombreInput.value)) {
        alert('El nombre solo puede contener caracteres alfabéticos, espacios o guiones.');
        valid = false;
    }
    // Validar el identificacion (valor monetario válido)
    const identificacionRegex = /^\d+$/;
    if (!identificacionRegex.test(identificacionInput.value)) {
        alert('El documento de identidad debe ser un valor numérico válido.');
        valid = false;
    }
    return valid;
}
