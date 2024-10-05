document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('insertMovimientoForm');
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Previene el envío normal del formulario
        
        const userId = document.getElementById('userId').value;
        const empleadoId = document.getElementById('empleadoId').value;
        const vdi = document.getElementById('vdi').value;
        const tipoMovimiento = document.getElementById('tipoMovimiento').value;
        const tiposStr = document.getElementById('tipos').value;
        let montoOriginal = parseFloat(document.getElementById('monto').value);
        const saldoVacaciones = parseFloat(document.getElementById('saldo').value);
        let monto = montoOriginal;
        let tipos = {};
        let tiposCorregido = "";
        let tipo = {};
        let TipoAccion = '';
        let credito = 1;
        let debito = -1;
        let nuevoSaldo = 0;

        //console.log('monto: ', monto);
        //console.log('saldoVacaciones: ', saldoVacaciones);
        //console.log('tipoMovimiento: ', tipoMovimiento);

        // Recorrer cada carácter del string original
        for (let i = 0; i < tiposStr.length; i++) {
            const char = tiposStr[i];

            // Reemplazar comillas simples por dobles y viceversa
            if (char === "'") {
                tiposCorregido += '"'; // Cambia comillas simples a dobles
            } else if (char === '"') {
                tiposCorregido += "'"; // Cambia comillas dobles a simples
            } else {
                tiposCorregido += char; // Agrega el carácter tal cual si no es una comilla
            }
        }

        tipos = JSON.parse(tiposCorregido);
        //console.log('tipos: ', tipos);

        // Ejemplo de uso
        for (let i = 0; i < tipos.length; i++) {
            const element = tipos[i];
            if (element.Id == tipoMovimiento) {
                tipo = element; // Asignar el valor a tipo
            }
        }

        //console.log('tipo: ', tipo);

        // Si existe el tipo, obtener el 'TipoAccion'
        TipoAccion = tipo.TipoAccion;
        //console.log('TipoAccion: ', TipoAccion);

        // Comparar si TipoAccion es 'Credito' o 'Debito'
        if (TipoAccion == 'Credito') {
            monto = credito * monto;
        } else if (TipoAccion == 'Debito') {
            monto = debito * monto;
        } 

        //console.log('montoOriginal: ', montoOriginal);
        //console.log('monto: ', monto);

        // Validar que el nuevo saldo no sea negativo
        nuevoSaldo = saldoVacaciones + monto; // Asumiendo que los movimientos positivos aumentan el saldo
        //console.log('nuevoSaldo: ', nuevoSaldo);

        /*if (nuevoSaldo < 0) {
            alert('Error: Monto del movimiento rechazado, el saldo sería negativo.');
            return;
        }*/

        try {
            const response = await fetch('/insertar_movimiento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userId, empleadoId, vdi, tipoMovimiento, monto, montoOriginal, nuevoSaldo })
            });

            const result = await response.json();

            if (result.success) {
                alert('Movimiento insertado exitosamente.');
                window.location.href = `/movimientos/${userId}/${vdi}`; // Redirigir a la lista de movimientos
            } else {
                console.error(result.error + ': ' + result.message);
                alert(result.error + ': ' + result.message);
            }
        } catch (error) {
            console.error('Error al insertar movimiento:', error);
            //alert('Hubo un error al insertar el movimiento.');
        }
    });
});
