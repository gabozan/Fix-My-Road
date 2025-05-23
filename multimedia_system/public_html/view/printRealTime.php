<div class="detection-container">
    <h1>Detección en tiempo real</h1>
    <div id="realtime-container">
        <video id="video" autoplay muted></video>
        <div>
            <button id="toggleCamara">Abrir Cámara</button>
            <button id="toggleTransmision" disabled>Iniciar Transmisión</button>
            <button id="terminarTodo" disabled>Terminar Todo</button>
        </div>
    </div>
    <div id="status"></div>

    <?php
        $nombreSesion = isset($_SESSION['id_user']) ? $_SESSION['id_user'] : 'none';
        echo "<script>const sessionName = " . json_encode($nombreSesion) . ";</script>";
    ?>

    <script src="assets/js/video.js"></script>
</div>
