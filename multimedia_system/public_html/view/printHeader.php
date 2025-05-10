<header>
    <div id="header-container">
        <div class="logo">
            <a href="index.php">
                <img src="./assets/imgs/logo_Fix-my-road_banner_no_background-white.png" alt="Fix-my-road Logo">
            </a>
        </div>

        <div class="dropdowns-tuple">
            <div class="options-actions">
                <div class="dropdown">
                    <a id="options-btn">
                        <img src="./assets/imgs/options-icon-white.png" alt="Opciones" width="100px">
                    </a>
                    <ul class="dropdown-menu" id="options-menu">
                        <li><a href="index.php?action=resource-ranking">Ranking</a></li>
                        <li><a href="index.php?action=resource-real-time">Detección en tiempo real</a></li>
                        <li><a href="index.php?action=resource-video-detect">Detección de video</a></li>
                        <li><a href="index.php?action=resource-image-detect">Detección de imagen</a></li>
                    </ul>
                </div>
            </div>

            <div class="user-actions">
                <div class="dropdown">
                    <a id="login-btn">
                        <img src="./assets/imgs/user-icon-white.png" alt="Inicio de Sesión" width="100px">
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
    </div>
</header>
