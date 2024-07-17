document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.registration-form');
    const selectField = document.querySelector('.choice-field');
    const submitButton = document.querySelector('.registration-form button');

    form.addEventListener('submit', function(event) {
        if (selectField.value === '') {
            event.preventDefault();
            alert('Please select a designation');
            selectField.focus();
        }
    });
});