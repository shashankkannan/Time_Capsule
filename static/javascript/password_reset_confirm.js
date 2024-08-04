document.addEventListener("DOMContentLoaded", function() {
    const changePasswordButton = document.getElementById("new-password-button");
    const inputs = document.querySelectorAll('.form-input');
    const newPasswordField = document.querySelector('#id_new_password1');
    const confirmNewPasswordField = document.querySelector('#id_new_password2');

    function displayMessage(elementId, show, message = "") {
        let messageElement = document.getElementById(elementId + 'Message');
        const fieldBlock = document.getElementById(elementId + 'Block'); // Get the respective block
        if (!messageElement) {
            messageElement = document.createElement('div');
            messageElement.id = elementId + 'Message';
            messageElement.classList.add('error-message');
        }
        messageElement.textContent = show ? message : '';
        if (fieldBlock.nextSibling) {
            fieldBlock.parentNode.insertBefore(messageElement, fieldBlock.nextSibling);
        } else {
            fieldBlock.parentNode.appendChild(messageElement);
        }
    }

    function validatePasswordSecurity(password) {
        if (password.length === 0) return ''; // No message if no input
        const minLength = 8;
        const digitPattern = /\d/;
        const upperCasePattern = /[A-Z]/;
        const lowerCasePattern = /[a-z]/;
        const specialCharPattern = /[!@#$%^&*(),.?":{}|<>]/;
        if (password.length < minLength) {
            return `Password must be at least ${minLength} characters long.`;
        } else if (!digitPattern.test(password)) {
            return "Password must contain at least one digit.";
        } else if (!upperCasePattern.test(password)) {
            return "Password must contain at least one uppercase letter.";
        } else if (!lowerCasePattern.test(password)) {
            return "Password must contain at least one lowercase letter.";
        } else if (!specialCharPattern.test(password)) {
            return "Password must contain at least one special character.";
        }
        return '';
    }

    function validateForm() {
        const allFilled = Array.from(inputs).every(input => input.value.trim() !== '');
        const passwordsMatch = newPasswordField.value === confirmNewPasswordField.value;
        const passwordSecurityMessage = validatePasswordSecurity(newPasswordField.value);

        // Enable the change password button if all conditions are met
        changePasswordButton.disabled = !(allFilled && passwordsMatch && passwordSecurityMessage === '');

        // Provide real-time feedback
        if (newPasswordField.value.length > 0) {
            displayMessage('newPassword', true, validatePasswordSecurity(newPasswordField.value));
        } else {
            displayMessage('newPassword', false);
        }

        if (!passwordsMatch && confirmNewPasswordField.value.trim() !== '') {
            confirmNewPasswordField.setCustomValidity("Passwords do not match.");
            newPasswordField.style.borderColor = confirmNewPasswordField.style.borderColor = '#DC143C';
            displayMessage('confirmNewPassword', true, "Passwords do not match.");
        } else {
            confirmNewPasswordField.setCustomValidity('');
            newPasswordField.style.borderColor = confirmNewPasswordField.style.borderColor = ''; // Reset border color
            displayMessage('confirmNewPassword', false);
        }
    }

    // Attach the validateForm function as an event listener to each input for real-time validation
    inputs.forEach(input => input.addEventListener('input', validateForm));

    // Initial call to validateForm to ensure correct initial state
    validateForm();

    document.querySelectorAll('.toggle-password').forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            const targetFieldId = this.parentNode.id === 'newPasswordBlock' ? 'id_new_password1' : 'id_new_password2';
            const passwordField = document.querySelector(`#${targetFieldId}`);
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    });
});