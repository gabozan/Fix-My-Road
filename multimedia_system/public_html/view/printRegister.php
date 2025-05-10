<?php if (!empty($errors)): ?>
    <div id="error-messages">
        <ul>
            <?php foreach ($errors as $error): ?>
                <li><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></li>
            <?php endforeach; ?>
        </ul>
    </div>
<?php endif; ?>

<div id="register-container">
    <div id="form-container">
        <form action="index.php?action=resource-register" method="post">
            <h2>Crear Cuenta</h2>
            
            <div class="input-container">
                <label for="name">Nombre de Usuario</label>
                <input type="text" name="name" required pattern="[A-Za-zÀ-ÿ\s]{1,}" title="Solo se permiten letras y espacios.">
            </div>

            <div class="input-container">
                <label for="email">Email</label>
                <input type="email" name="email" required title="Introduce un correo válido.">
            </div>

            <div class="input-container">
                <label for="password">Contraseña</label>
                <input type="password" name="password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>

            <input type="submit" value="Registrar">
        </form>

        <div class="google-login">
            <div class="line-with-text">
                <span>o</span>
            </div>

            <a href="URL_DE_GOOGLE_AUTH" class="google-button">
                <img src="./assets/imgs/google-icon.png" alt="Iniciar sesión con Google">
            </a>
        </div>

        <div class="login">
            <p>Ya tengo cuenta <a href="index.php?action=resource-login"> Iniciar Sesión </a></p>
        </div>

    </div>
</div>
