JavaScript 

const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginButton = document.getElementById('login-button');
const errorMessage = document.getElementById('error-message');

loginButton.addEventListener('click', (e) => {
    e.preventDefault();
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (username && password) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/dashboard';
            } else {
                errorMessage.textContent = data.message;
            }
        })
        .catch(error => {
            errorMessage.textContent = 'An error occurred. Please try again.';
        });
    } else {
        errorMessage.textContent = 'Please fill in both username and password.';
    }
});

window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    if (width < 768) {
        loginForm.style.flexDirection = 'column';
    } else {
        loginForm.style.flexDirection = 'row';
    }
});