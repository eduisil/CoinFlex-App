// document.addEventListener('DOMContentLoaded', function () {
//     const loginForm = document.getElementById('login-form');
//     const errorMessage = document.getElementById('error-message');

//     loginForm.addEventListener('submit', async function (event) {
//         event.preventDefault();

//         const formData = new FormData(loginForm);
//         const username = formData.get('username');
//         const password = formData.get('password');

//         try {
//             const response = await fetch('/token', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                 },
//                 body: new URLSearchParams({
//                     username: username,
//                     password: password
//                 }),
//             });

//             if (!response.ok) {
//                 throw new Error('Login failed');
//             }

//             const data = await response.json();
//             // Guardar el token en localStorage o cookies
//             localStorage.setItem('token', data.access_token);
//             // Redirigir a la página protegida
//             window.location.href = 'index.html';
//         } catch (error) {
//             errorMessage.textContent = 'Incorrect username or password xd';
//         }
//     });
// });
