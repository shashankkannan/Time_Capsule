document.addEventListener("DOMContentLoaded", function() {
    // Toggle password visibility
    document.querySelector('.toggle-password').addEventListener('click', function(e) {
        // toggle the type attribute
        const passwordField = document.querySelector('#id_password');
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // toggle the eye / eye slash icon
        this.classList.toggle('fa-eye-slash');
    });
});