document.getElementById('language-select').addEventListener('change', function() {
    var selectedValue = this.value; // Get the selected value
    languageChoice(selectedValue);  // Call your function with the selected value
});

function languageChoice(choice) {
    // Send an HTTP request to the server with the user's choice
    fetch(`/language?choice=${choice}`)
        .then(() => {
            // Refresh the user's current webpage
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
}