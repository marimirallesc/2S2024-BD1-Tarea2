
function validaciones() {
    const nombreInput = document.getElementById('nombre');
    const vdiInput = document.getElementById('vdi');

    let valid = true;

    // Validar el nombre (solo caracteres alfabéticos y espacios)
    const nombreRegex = /^[A-Za-z\s-]+$/;
    if (!nombreRegex.test(nombreInput.value)) {
        alert('El nombre solo puede contener caracteres alfabéticos, espacios o guiones.');
        valid = false;
    }
    // Validar el vdi (valor monetario válido)
    const vdiRegex = /^\d+(\.\d{1,2})?$/;
    if (!vdiRegex.test(vdiInput.value)) {
        alert('El documento de identidad debe ser un valor numérico válido.');
        valid = false;
    }
    return valid;
}
