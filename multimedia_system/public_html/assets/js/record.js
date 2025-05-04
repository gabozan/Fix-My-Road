const preview  = document.getElementById('preview');
const startBtn = document.getElementById('startBtn');
const stopBtn  = document.getElementById('stopBtn');
const status   = document.getElementById('status');

let mediaRecorder;
let chunks = [];

async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    preview.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop        = onRecordingStop;
    startBtn.disabled = false;
  } catch (err) {
    status.textContent = '⚠️ No se pudo acceder a la cámara: ' + err.message;
  }
}

initCamera(); 
startBtn.addEventListener('click', () => {
  chunks = [];
  mediaRecorder.start();
  startBtn.disabled = true;
  stopBtn.disabled  = false;
  status.textContent = '🔴 Grabando…';
});

stopBtn.addEventListener('click', () => {
  mediaRecorder.stop();
  stopBtn.disabled  = true;
  status.textContent = 'Deteniendo…';
});

async function onRecordingStop() {
  status.textContent = '➡️ Preparando vídeo para subir…';
  const blob = new Blob(chunks, { type: 'video/webm' });

  try {
    const resp = await fetch(
      'https://europe-southwest1-fixmyroad-458407.cloudfunctions.net/uploadVideo',
      {
        method: 'POST',
        headers: { 'Content-Type': 'video/webm' },
        body: blob
      }
    );
    const result = await resp.json();
    if (resp.ok) {
      status.innerHTML = `✅ Subido: <code>${result.filename}</code> (${result.size} bytes)`;
    } else {
      throw new Error(result.error || resp.statusText);
    }
  } catch (err) {
    status.textContent = '❌ Error subiendo: ' + err.message;
  } finally {
    startBtn.disabled = false;
  }
}
