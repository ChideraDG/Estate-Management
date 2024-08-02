document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');

    if (form) {  // Check if the form exists in the DOM
        const loadingIndicator = document.getElementById('loadingIndicator');
        const errorMessage = document.getElementById('errorMessage');
        const sentMessage = document.getElementById('sentMessage');

        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            loadingIndicator.style.display = 'block';
            errorMessage.style.display = 'none';
            sentMessage.style.display = 'none';

            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                loadingIndicator.style.display = 'none';
                if (data.success) {
                    sentMessage.style.display = 'block';
                    form.reset(); // Optional: reset the form fields
                } else {
                    errorMessage.innerText = data.error || 'An error occurred. Please try again.';
                    errorMessage.style.display = 'block';
                }
            })
            .catch(error => {
                loadingIndicator.style.display = 'none';
                errorMessage.innerText = 'An error occurred. Please try again.';
                errorMessage.style.display = 'block';
            });
        });
    }
});
