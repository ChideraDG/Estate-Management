document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    const designationField = document.querySelector('select[name="designation"]');
    const agreeTermCheckbox = document.getElementById('agree-term');

    form.addEventListener('submit', function(event) {
        let valid = true;

        // Check if a designation is selected
        if (designationField.value === '') {
            alert('Please select a valid designation.');
            valid = false;
        }

        // Check if the terms and conditions checkbox is checked
        if (!agreeTermCheckbox.checked) {
            alert('You must agree to the terms and conditions.');
            valid = false;
        }

        if (!valid) {
            event.preventDefault(); // Prevent form submission
        }
    });
});