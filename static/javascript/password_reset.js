document.addEventListener("DOMContentLoaded", function() {
    const sendResetEmailButton = document.getElementById("send-reset-email-button");
    const emailInput = document.querySelector('.form-input');

    // Function to enable the send email button if the email field is not empty
    function validateEmailField() {
        // Trim leading and trailing whitespace and check if it's not empty
        sendResetEmailButton.disabled = !emailInput.value.trim();
    }

    // Attach the validateEmailField function as an event listener to the email input for real-time validation
    emailInput.addEventListener('input', validateEmailField);

    // Initial call to validateEmailField to ensure correct initial state
    validateEmailField();
});