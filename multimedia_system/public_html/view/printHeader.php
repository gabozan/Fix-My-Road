<header>
    <div id="header-container">
        <div class="logo">
            <a href="">
                <img src="/assets/imgs/logo_Fix-my-road_banner_no_background.png" alt="Fix-my-road Logo">
            </a>
        </div>

        <div class="home-button">
            <a href="">Inicio</a>
        </div>
        
        <div class="user-actions">
            <div class="dropdown">
                <a id="login-btn">
                    <img src="/assets/imgs/user-icon.png" alt="Inicio de Sesión" width="100px">
                </a>
                <ul class="dropdown-menu" id="user-menu">
                    <?php if ($isLoggedIn): ?>
                        <li><a href="index.php?action=resource-myAccount">Mi cuenta</a></li>
                        <li><a href="index.php?action=logout">Cerrar sesión</a></li>
                    <?php else: ?>
                        <li><a href="index.php?action=resource-login">Iniciar sesión</a></li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>

    </div>
</header>