<?php
$name = isset($_GET['name']) ? $_GET['name'] : '';
$email = isset($_GET['email']) ? $_GET['email'] : '';
?>

<div id="register-container">
    <div id="form-container">
        <form action="index.php?action=resource_register_google" method="post">
            <h2>Establecer una Contraseña</h2>
            <div class="input-container">
                <label for="password">Contraseña</label>
                <input type="password" name="password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>

            <input type="submit" value="Registrar">
            <input type="hidden" name="name" value="<?php echo htmlspecialchars($name); ?>">
            <input type="hidden" name="email" value="<?php echo htmlspecialchars($email); ?>">
        </form>
    </div>
</div>

