// Get the error message element
const errorMessageElement = document.getElementById('error-message');

// Function to show error message
function showError_message(message) {
    if (errorMessageElement) {
        errorMessageElement.innerText = message;
        errorMessageElement.style.display = 'block';
    }
}

// Function to hide error message
function hideErrorMessage() {
    if (errorMessageElement) {
        errorMessageElement.style.display = 'none';
    }
}

// Get the login form
const loginForm = document.getElementById('login-form');

// Add event listener to the login form
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Basic form validation
        if (username === '' || password === '') {
            showError_message('Please fill in all fields');
        } else {
            // Send a POST request to the server with the username and password
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Login successful, redirect to the next page
                    window.location.href = '/dashboard';
                } else {
                    showError_message(data.message);
                }
            })
            .catch(error => {
                console.error(error);
                showError_message('An error occurred');
            });
        }
    });
}