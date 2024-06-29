const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkMode = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

document.querySelectorAll('.sidebar a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        //e.preventDefault(); // Evita la acción predeterminada del enlace
        document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
        this.classList.add('active');
    });
});

const darkModeToggle = darkMode;

// Verificar el estado actual del modo oscuro al cargar la página
window.addEventListener('load', () => {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDarkMode);
});

function setDarkMode(isDarkMode) {
    document.body.classList.toggle('dark-mode-variables', isDarkMode);
    if (!isDarkMode) {
        darkModeToggle.querySelector('span:nth-child(1)').classList.toggle('active');
        darkModeToggle.querySelector('span:nth-child(2)').classList.toggle('active', false);
    } else {
        darkModeToggle.querySelector('span:nth-child(2)').classList.toggle('active');
        darkModeToggle.querySelector('span:nth-child(1)').classList.toggle('active', false);
    }
    localStorage.setItem('darkMode', isDarkMode);
}

darkModeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.contains('dark-mode-variables');
    setDarkMode(!isDarkMode);
});

document.getElementById('cerrar_sesion').addEventListener('click', function(e) {
    localStorage.removeItem('darkMode');
});
