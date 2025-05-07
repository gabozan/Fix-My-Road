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

function stopGeolocation() {
  if (watchId != null) navigator.geolocation.clearWatch(watchId);
}

let lastLoggedSecond = -1;

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

btnCamara.addEventListener('click', async () => {
  if (!camaraActiva) {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      video.srcObject = stream;
      camaraActiva = true;
      btnCamara.textContent = 'Cerrar Cámara';
      btnTransmision.disabled = false;
      btnTerminar.disabled = false;

      mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
      mediaRecorder.ondataavailable = e => chunks.push(e.data);
      mediaRecorder.onstop = onRecordingStop;
    } catch (err) {
      console.error('Error al abrir la cámara:', err);
    }
  } else {
    cerrarCamara();
  }
});

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
  } else if (mediaRecorder.state === 'paused') {
    mediaRecorder.resume();
    transmisionActiva = true;
    btnTransmision.textContent = 'Pausar Transmisión';
  }
});

btnTerminar.addEventListener('click', () => {
  cerrarCamara();
  if (mediaRecorder && grabando) {
    grabando = false;
    mediaRecorder.stop();
    stopGeolocation();
    status.textContent = '⏳ Deteniendo y subiendo...';
  }
});

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
}

async function onRecordingStop() {
  const videoBlob = new Blob(chunks, { type: 'video/webm' });

  try {
    const videoResp = await fetch(
      'https://europe-southwest1-fixmyroad-458407.cloudfunctions.net/uploadVideo/upload-video',
      {
        method: 'POST',
        headers: { 'Content-Type': 'video/webm' },
        body: videoBlob
      }
    );
    const videoResult = await videoResp.json();
    if (!videoResp.ok) throw new Error(videoResult.error || videoResp.statusText);
    status.textContent = '📤 Vídeo subido, subiendo posiciones...';

    const posResp = await fetch(
      'https://europe-southwest1-fixmyroad-458407.cloudfunctions.net/uploadVideo/upload-positions',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(positions)
      }
    );
    const posResult = await posResp.json();
    if (!posResp.ok) throw new Error(posResult.error || posResp.statusText);

    status.innerHTML = `✅ Vídeo subido: <code>${videoResult.filename}</code><br>
                        ✅ Posiciones subidas: <code>${posResult.filename}</code><br>
                        📍 Puntos GPS: ${positions.length}`;
  } catch (err) {
    status.textContent = '❌ Error subiendo: ' + err.message;
  }
}
