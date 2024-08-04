document.addEventListener('DOMContentLoaded', function() {
    // Get the message from the data attribute
    const messageElement = document.getElementById('lastVisitMessage');
    const message = messageElement.getAttribute('data-message');

    if (message !== "None") {
        messageElement.textContent = message;
        showPopup();
    }
});

function showPopup() {
    document.getElementById('welcomePopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('welcomePopup').style.display = 'none';
}