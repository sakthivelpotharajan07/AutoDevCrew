class User {
    constructor(username, password) {
        this.username = username;
        this.password = password;
    }

    authenticateUser() {
        // Call the API to authenticate the user
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: this.username,
                password: this.password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // User is authenticated, save the token
                localStorage.setItem('token', data.token);
                window.location.href = '/dashboard';
            } else {
                // User is not authenticated, display an error message
                document.getElementById('error-message').innerText = 'Invalid username or password';
            }
        })
        .catch(error => {
            console.error('Error authenticating user:', error);
            document.getElementById('error-message').innerText = 'Error authenticating user';
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const user = new User(username, password);
        user.authenticateUser();
    });
});