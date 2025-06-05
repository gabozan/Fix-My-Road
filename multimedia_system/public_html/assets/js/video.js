const video = document.getElementById('video'); 
const btnCamara = document.getElementById('toggleCamara');
const btnTransmision = document.getElementById('toggleTransmision');
const btnTerminar = document.getElementById('terminarTodo');
const status = document.getElementById('status');

let stream = null;
let camaraActiva = false;
let transmisionActiva = false;
let grabando = false;
let mediaRecorder;
let chunks = [];
let positions = [];
let lastPosition = null;
let watchId = null;

// Esta función activa el seguimiento GPS en tiempo real, guardando la última posición en cada cambio.
// Usa `navigator.geolocation.watchPosition`.
function startGeolocation() {
  if (!navigator.geolocation) {
    status.textContent = '⚠️ Geolocalización no soportada.';
    return;
  }
  watchId = navigator.geolocation.watchPosition(
    pos => lastPosition = pos.coords,
    err => console.warn('GPS error:', err.message),
    { enableHighAccuracy: true, maximumAge: 0, timeout: 10000 }
  );
}

// Detiene la captura continua del GPS, limpiando el watcher activo.
function stopGeolocation() {
  if (watchId != null) navigator.geolocation.clearWatch(watchId);
}

let lastLoggedSecond = -1;

// Esta función se ejecuta en cada frame del video usando `requestVideoFrameCallback`.
// Si está grabando y hay GPS disponible, guarda una posición por segundo.
function handleFrame(now, metadata) {
  if (!grabando) return;

  const currentSecond = Math.floor(metadata.mediaTime);
  if (lastPosition && currentSecond !== lastLoggedSecond) {
    lastLoggedSecond = currentSecond;
    positions.push({
      mediaTime: metadata.mediaTime,
      latitude: lastPosition.latitude,
      longitude: lastPosition.longitude
    });
  }

  video.requestVideoFrameCallback(handleFrame);
}

async function abrirCamaraTrasera() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(d => d.kind === 'videoinput');

    // Intentar encontrar cámara trasera por etiqueta
    let backCamera = videoDevices.find(device =>
      device.label.toLowerCase().includes('back') ||
      device.label.toLowerCase().includes('rear')
    );

    let constraints;

    if (backCamera) {
      // Si hay cámara trasera identificada, usar deviceId exacto
      constraints = { video: { deviceId: { exact: backCamera.deviceId } }, audio: true };
    } else {
      // Si no, usar facingMode: environment (más compatible en móviles)
      constraints = { video: { facingMode: { ideal: 'environment' } }, audio: true };
    }

    stream = await navigator.mediaDevices.getUserMedia(constraints);

    video.srcObject = stream;
    camaraActiva = true;
    btnCamara.textContent = 'Cerrar Cámara';
    btnTransmision.disabled = false;
    btnTerminar.disabled = false;

    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = onRecordingStop;
    status.textContent = '📷 Cámara trasera activa.';
  } catch (err) {
    console.error('Error al abrir la cámara trasera:', err);
    status.textContent = '❌ No se pudo acceder a la cámara trasera.';
  }
}

btnCamara.addEventListener('click', async () => {
  if (!camaraActiva) {
    await Trasera(abrirCamara);
  } else {
    cerrarCamara();
  }
});

// Controla la grabación con MediaRecorder.
// Inicia desde cero si no se estaba grabando, o pausa/reanuda según corresponda.
// También inicia el GPS y el seguimiento por frame.
btnTransmision.addEventListener('click', () => {
  if (!mediaRecorder) return;
  if (!grabando) {
    chunks = [];
    positions = [];
    lastPosition = null;
    grabando = true;
    mediaRecorder.start();
    startGeolocation();
    video.requestVideoFrameCallback(handleFrame);
    transmisionActiva = true;
    btnTransmision.textContent = 'Pausar Transmisión';
    status.textContent = '🔴 Grabando…';
  } else if (mediaRecorder.state === 'recording') {
    mediaRecorder.pause();
    transmisionActiva = false;
    btnTransmision.textContent = 'Reanudar Transmisión';
    status.textContent = '⏸ Transmisión pausada.';
  } else if (mediaRecorder.state === 'paused') {
    mediaRecorder.resume();
    transmisionActiva = true;
    btnTransmision.textContent = 'Pausar Transmisión';
    status.textContent = '🔴 Grabando…';
  }
});

// Detiene la cámara y la grabación, y luego llama al proceso de subida de datos.
btnTerminar.addEventListener('click', () => {
  cerrarCamara();
  if (mediaRecorder && grabando) {
    grabando = false;
    mediaRecorder.stop();
    stopGeolocation();
    status.textContent = '⏳ Deteniendo y subiendo...';
  }
});

// Detiene todas las pistas del stream (video/audio).
// También reinicia los botones y variables.
function cerrarCamara() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    stream = null;
  }
  camaraActiva = false;
  grabando = false;
  btnCamara.textContent = 'Abrir Cámara';
  btnTransmision.disabled = true;
  btnTerminar.disabled = true;
  status.textContent = '📷 Cámara cerrada.';
}

// Sube el array de posiciones GPS como JSON a una función en la nube.
// Luego sube el video como Blob con otro nombre base.
async function onRecordingStop() {
  const videoBlob = new Blob(chunks, { type: 'video/webm' });
  const timestamp = Date.now();
  const baseVideoName     = `${sessionName}_${timestamp}_video`;
  const basePositionsName = `${sessionName}_${timestamp}_positions`;

  try {
    status.textContent = '📤 Subiendo posiciones…';
    const posResp = await fetch(
      `https://europe-southwest1-fixmyroad-458407.cloudfunctions.net/uploadVideo/upload-positions`
      + `?basePositionsName=${encodeURIComponent(basePositionsName)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(positions)
      }
    );
    const posResult = await posResp.json();
    if (!posResp.ok) throw new Error(posResult.error || posResp.statusText);

    status.textContent = '✅ Posiciones subidas, subiendo vídeo…';

    const videoResp = await fetch(
      `https://europe-southwest1-fixmyroad-458407.cloudfunctions.net/uploadVideo/upload-video`
      + `?baseVideoName=${encodeURIComponent(baseVideoName)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'video/webm' },
        body: videoBlob
      }
    );
    const videoResult = await videoResp.json();
    if (!videoResp.ok) throw new Error(videoResult.error || videoResp.statusText);

    status.innerHTML = `
      ✅ Vídeo subido: <code>${videoResult.filename}</code><br>
      ✅ Posiciones subidas: <code>${posResult.filename}</code><br>
      📍 Puntos GPS: ${positions.length}
    `;
  } catch (err) {
    status.textContent = '❌ Error subiendo: ' + err.message;
  }
}
