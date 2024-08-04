document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.getElementById('logout-link');

    logoutLink.addEventListener('click', function(event) {
        // Prevent the default link behavior
        event.preventDefault();

        // Show a confirmation dialog
        const userConfirmed = confirm('Are you sure you want to log out?');

        // If the user clicked "OK", proceed with the logout
        if (userConfirmed) {
            window.location.href = this.href;
        }
    });
});