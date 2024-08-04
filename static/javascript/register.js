document.addEventListener("DOMContentLoaded", function() {
    const signupButton = document.getElementById("signup-button");
    const inputs = document.querySelectorAll('.form-input');
    const passwordField = document.querySelector('#id_password');
    const confirmPasswordField = document.querySelector('#id_confirm_password');

    function displayPasswordMismatchMessage(show) {
        let messageElement = document.getElementById('passwordMismatchMessage');
        const confirmPasswordBlock = document.getElementById('confirmPasswordBlock'); // Get the confirm password block
        if (!messageElement) {
            messageElement = document.createElement('div');
            messageElement.id = 'passwordMismatchMessage';
            messageElement.classList.add('error-message'); // Use a class for styling if you prefer
        }
        messageElement.textContent = show ? "Passwords do not match." : '';
        if (confirmPasswordBlock.nextSibling) {
            confirmPasswordBlock.parentNode.insertBefore(messageElement, confirmPasswordBlock.nextSibling);
        } else {
            confirmPasswordBlock.parentNode.appendChild(messageElement);
        }
    }

    // Function to check if all fields are filled and passwords match
    function validateForm() {
        const allFilled = Array.from(inputs).every(input => input.value.trim() !== '');
        const passwordsMatch = passwordField.value === confirmPasswordField.value;

        // Enable the signup button if all conditions are met
        signupButton.disabled = !(allFilled && passwordsMatch);

        // Provide real-time feedback about password match
        if (!passwordsMatch && confirmPasswordField.value.trim() !== '') {
            // This condition checks if the confirm password field is not empty and passwords do not match
            // Update this to show your error message or indication as needed
            confirmPasswordField.setCustomValidity("Passwords do not match.");
            passwordField.style.borderColor = confirmPasswordField.style.borderColor = '#DC143C'; // Example red color for error
            displayPasswordMismatchMessage(true);
        } else {
            // If passwords match or confirm password field is empty, clear the custom validity message
            confirmPasswordField.setCustomValidity('');
            passwordField.style.borderColor = confirmPasswordField.style.borderColor = ''; // Reset to default or original border color
            // Hide the error message
            displayPasswordMismatchMessage(false);
        }
    }

    // Attach the validateForm function as an event listener to each input for real-time validation
    inputs.forEach(input => input.addEventListener('input', validateForm));

    // Initial call to validateForm to ensure correct initial state
    validateForm();

    document.querySelectorAll('.toggle-password').forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            const targetFieldId = this.parentNode.id === 'passwordBlock' ? 'id_password' : 'id_confirm_password';
            const passwordField = document.querySelector(`#${targetFieldId}`);
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    });
});