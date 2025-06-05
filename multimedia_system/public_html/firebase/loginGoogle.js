// Este script inicializa Firebase y configura el login con Google usando un popup.
// Al hacer clic en el botón con ID 'google-login', se autentica al usuario y redirige a la página PHP con sus datos.
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-auth.js";

// Configuración e inicialización de la app Firebase
initializeApp({
    apiKey: "AIzaSyCN24no0cO6RyiFTwRSawgzdVQU2dSR_Vk",
    authDomain: "fixmyroad-458407.firebaseapp.com",
    projectId: "fixmyroad-458407",
    storageBucket: "fixmyroad-458407.firebasestorage.app",
    messagingSenderId: "322599195853",
    appId: "1:322599195853:web:69cf06bf0dc5ec7bf64584"
});

// Asocia el evento de clic al botón de login con Google
document.getElementById('google-login').addEventListener('click', () => {
    signInWithPopup(getAuth(), new GoogleAuthProvider())
        .then((result) => {
            const user = result.user;
            // Redirige al backend PHP pasando nombre y email del usuario autenticado
            const url = `index.php?action=resource_login_google&name=${encodeURIComponent(user.displayName)}&email=${encodeURIComponent(user.email)}`;
            window.location.href = url;
        })
        .catch((error) => {
            // Manejo de errores durante el login
            console.error('Error signing in:', error.code, error.message);
        });
});
