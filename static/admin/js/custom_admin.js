/* custom_admin.js */

// Example of a small JavaScript function to alert when saving the FAQ
document.addEventListener('DOMContentLoaded', function () {
    const saveButton = document.querySelector('input[name="_save"]');
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            alert("Your FAQ is being saved!");
        });
    }
});
