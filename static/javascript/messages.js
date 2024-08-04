document.addEventListener('DOMContentLoaded', (event) => {
    const messages = document.querySelectorAll('.toast');
    messages.forEach((message) => {
        message.addEventListener('animationend', () => {
            message.remove();
        });
    });
});