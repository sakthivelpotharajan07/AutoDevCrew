const loginForm = document.querySelector('.login-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    if (!username || !password) {
        document.querySelector('.error-message').innerText = 'Please fill in both username and password';
        return;
    }

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                window.location.href = '/dashboard';
            } else {
                document.querySelector('.error-message').innerText = data.message;
            }
        } else {
            document.querySelector('.error-message').innerText = 'Server error';
        }
    } catch (error) {
        document.querySelector('.error-message').innerText = 'Network error';
    }
});