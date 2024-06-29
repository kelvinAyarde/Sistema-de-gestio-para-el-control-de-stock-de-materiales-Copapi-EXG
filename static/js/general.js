const url_servidor = "http://127.0.0.1:5000";

window.addEventListener("DOMContentLoaded", (event) => {
    const cerrarBtn = document.getElementById('cerrar-btn');
    if (cerrarBtn) {
        cerrarBtn.addEventListener('click', function() {
            const popup = document.querySelector('.cont_pantalla_emergente main');
            const overlay = document.getElementById('popup-overlay');
            if (popup) popup.remove();
            if (overlay) overlay.style.display = 'none';
        });
    }
});

function crearMensaje(titulo, mensaje, redireccion) {
    const contenedor = document.getElementById('mensaje');
    const overlay = document.getElementById('popup-overlay');
    
    // Verifica si el contenedor ya tiene algún mensaje
    if (contenedor.children.length > 0) {
        return; // Si ya hay un mensaje, no hace nada
    }

    const popup = document.createElement('div');
    popup.classList.add('popup', titulo);
    
    const popupTitulo = document.createElement('h2');
    popupTitulo.textContent = titulo;
    
    const popupMensaje = document.createElement('p');
    popupMensaje.textContent = mensaje;
    
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Cerrar';
    closeButton.classList.add('close-btn');
    
    closeButton.addEventListener('click', function() {
        popup.remove();
        overlay.style.display = 'none';
        if (redireccion) {
            window.location.href = redireccion;
        }
    });

    popup.append(popupTitulo, popupMensaje, closeButton);
    contenedor.append(popup);
    overlay.style.display = 'block';
}

/*
function BuscarEnTabla(tabla, textoBusqueda) {
    const rows = document.querySelectorAll(`${tabla} tbody tr`);
    rows.forEach(row => {
        let coincide = false;
        row.querySelectorAll('td').forEach(td => {
            if (td.textContent.toLowerCase().includes(textoBusqueda.toLowerCase())) {
                coincide = true;
            }
        });
        row.style.display = coincide ? '' : 'none';
    });
}*/

function agregarAsteriscosARequeridos() {
    const requiredInputs = document.querySelectorAll('input[required]');
    requiredInputs.forEach(input => {
        let label = document.querySelector(`label[for="${input.id}"]`);
        if (!label) {
            label = document.createElement('label');
            label.setAttribute('for', input.id);
            input.parentNode.insertBefore(label, input);
        }
        if (!label.innerHTML.includes('<span style="color: red;">*</span>')) {
            label.innerHTML += ' <span style="color: red;">*</span>';
        }
    });
}
/*
document.addEventListener('DOMContentLoaded', function() {
    agregarAsteriscosARequeridos();

    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                agregarAsteriscosARequeridos();
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
*/