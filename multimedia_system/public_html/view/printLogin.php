<?php if (!empty($errors)): ?>
    <div id="error-messages">
        <ul>
            <?php foreach ($errors as $error): ?>
                <li><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></li>
            <?php endforeach; ?>
        </ul>
    </div>
<?php endif; ?>
<div id="login-container">
    <div id="form-container">
        <form action="index.php?action=resource-login" method="post">
            <h2>Iniciar Sesión</h2>

            <div class="input-container">
                <label for="email">Email</label> <br>
                <input type="email" name="email" required title="Introduce un correo válido.">
            </div>

            <div class="input-container">
                <label for="password">Contraseña</label> <br>
                <input type="password" name="password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>
            
            <input type="submit" value="Enviar">
        </form>

        <div class="registrar">
            <p>No tengo cuenta <a href="index.php?action=resource-register"> Crear una cuenta</a></p>
        </div>

    </div>
</div>