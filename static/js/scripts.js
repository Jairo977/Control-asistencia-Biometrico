window.addEventListener('load', function() {
    const sidebarLogo = document.querySelector('.sidebar-logo');
    const loginLogo = document.querySelector('.login-logo');

    if (sidebarLogo) {
        sidebarLogo.onerror = function() {
            // Usar una imagen por defecto o mostrar un placeholder
            this.style.display = 'none';
        };
    }

    if (loginLogo) {
        loginLogo.onerror = function() {
            // Usar una imagen por defecto o mostrar un placeholder
            this.style.display = 'none';
        };
    }
});
