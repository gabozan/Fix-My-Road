<div id="account-container">
    <div id="form-container">
        <form action="index.php?action=update-user-info" method="post" enctype="multipart/form-data">
            <h2>Editar Información de Cuenta</h2>
            <h3>Foto de Perfil</h3>
            <div class="profile-picture-container">
                <img src="<?php echo $filesPublicPath . ($userData['profile_picture'] ?? 'default_profile_picture.png'); ?>"
                    alt="Foto de perfil" id="profile-picture-preview" class="profile-picture-preview">
            </div>
            <br>
            <div class="input-container">
                <label for="profile_picture">Subir Foto</label> <br>
                <input type="file" name="profile_picture" accept="image/*">
            </div>
            
            <h3>Información de Cuenta</h3>
            <div class="input-container">
                <label for="email">Correo Electrónico</label> <br>
                <input type="email" name="email" value="<?php echo htmlentities($userData['email'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?>" required title="Introduce un correo válido.">
            </div>

            <div class="input-container">
                <label for="password">Nueva Contraseña</label> <br>
                <input type="password" name="password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>

            <div class="input-container">
                <label for="confirm_password">Confirmar Contraseña</label> <br>
                <input type="password" name="confirm_password" required pattern="[A-Za-z0-9]{1,}" title="Debe contener solo caracteres alfanuméricos.">
            </div>

            <h3>Información Personal</h3>
            <div class="input-container">
                <label for="name">Nombre</label> <br>
                <input type="text" name="name" value="<?php echo htmlentities($userData['name'], ENT_QUOTES | ENT_HTML5, 'UTF-8'); ?>" required pattern="[A-Za-zÀ-ÿ\s]{1,}" title="Solo se permiten letras y espacios.">
            </div>

            <input type="submit" value="Guardar Cambios">
        </form>
    </div>
</div>
