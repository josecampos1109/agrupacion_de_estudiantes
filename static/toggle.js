// Script para alternar entre el modo oscuro y claro
const toggleSwitch = document.getElementById('darkModeToggle');
const body = document.body;

// Verifica si el usuario ya tiene preferencia de modo guardada
const currentMode = localStorage.getItem('dark-mode');
if (currentMode === 'enabled') {
    body.classList.add('dark-mode');
    toggleSwitch.checked = true;
}

// Evento de cambio en el interruptor
toggleSwitch.addEventListener('change', function () {
    if (this.checked) {
        body.classList.add('dark-mode');
        localStorage.setItem('dark-mode', 'enabled');
    } else {
        body.classList.remove('dark-mode');
        localStorage.setItem('dark-mode', 'disabled');
    }
});
