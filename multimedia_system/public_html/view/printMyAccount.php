<?php
$errors = $_SESSION['update_user_errors'] ?? [];
$oldValues = $_SESSION['update_user_old'] ?? [];
unset($_SESSION['update_user_errors'], $_SESSION['update_user_old']);
?>

<?php if (!empty($errors)): ?>
    <div id="error-messages">
        <ul>
            <?php foreach ($errors as $error): ?>
                <li><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></li>
            <?php endforeach; ?>
        </ul>
    </div>
<?php endif; ?>
<div id="account-container">
    <div id="form-container">
        <h2>Información de Cuenta</h2>
        <form action="index.php?action=update-user-info" method="post" enctype="multipart/form-data">
            <h3>Editar Información</h3>
            <div class="input-container">
                <label for="name">Nombre de Usuario</label> <br>
                <input type="text" name="name" value="<?php echo htmlentities($userData['name'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?>" required pattern="[A-Za-zÀ-ÿ\s]{1,}" title="Solo se permiten letras y espacios.">
            </div>

            <div class="input-container">
                <label for="email">Correo Electrónico</label> <br>
                <input type="email" name="email" value="<?php echo htmlentities($userData['email'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?>" required title="Introduce un correo válido.">
            </div>         

            <input type="submit" value="Guardar Cambios">
        </form>
        <form action="index.php?action=update-pass-info" method="post" enctype="multipart/form-data">
            <h3>Cambiar contraseña</h3>
            <div class="input-container">
                <label for="password">Nueva Contraseña</label> <br>
                <input type="password" name="password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>

            <div class="input-container">
                <label for="confirm_password">Confirmar Contraseña</label> <br>
                <input type="password" name="confirm_password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>            

            <input type="submit" value="Guardar Contraseña">
        </form>
    </div>
</div>
