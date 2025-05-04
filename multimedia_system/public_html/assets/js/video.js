const video = document.getElementById('video');
const btnCamara = document.getElementById('toggleCamara');
const btnTransmision = document.getElementById('toggleTransmision');
const btnTerminar = document.getElementById('terminarTodo');
const realtimeContainer = document.getElementById('realtime-container');

let stream = null;
let camaraActiva = false;
let transmisionActiva = false;
let procesamientoCompletado = false;

let mediaRecorder;
let chunks = [];
let grabando = false;

const resultadoDiv = document.createElement('div');
resultadoDiv.id = 'resultado-procesamiento';
resultadoDiv.classList.add('resultado-procesamiento');
resultadoDiv.style.display = 'none';
realtimeContainer.insertAdjacentElement('afterend', resultadoDiv);

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

      // Aquí va el evento onstop correctamente definido
      mediaRecorder.onstop = async () => {
        grabando = false;
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

          procesamientoCompletado = resp.ok;
          mostrarResultadoYBotonRefrescar(result);
        } catch (err) {
          console.error('❌ Error subiendo:', err.message);
          procesamientoCompletado = false;
          mostrarResultadoYBotonRefrescar();
        }
      };

    } catch (err) {
      console.error('Error al abrir la cámara:', err);
    }
  } else {
    cerrarCamara();
  }
});

btnTransmision.addEventListener('click', () => {
  if (!mediaRecorder) return;

  // Iniciar grabación si no está activa
  if (!grabando) {
    chunks = [];
    mediaRecorder.start();
    grabando = true;
    transmisionActiva = true;
    btnTransmision.textContent = 'Pausar Transmisión';
    console.log('🎥 Grabación iniciada');
  }
  // Pausar si está grabando
  else if (mediaRecorder.state === 'recording') {
    mediaRecorder.pause();
    transmisionActiva = false;
    btnTransmision.textContent = 'Reanudar Transmisión';
    console.log('⏸️ Grabación pausada');
  }
  // Reanudar si estaba pausada
  else if (mediaRecorder.state === 'paused') {
    mediaRecorder.resume();
    transmisionActiva = true;
    btnTransmision.textContent = 'Pausar Transmisión';
    console.log('▶️ Grabación reanudada');
  }

  actualizarBordeVideo();
});

btnTerminar.addEventListener('click', () => {
  cerrarCamara();
  transmisionActiva = false;
  actualizarBordeVideo();

  btnCamara.style.display = 'none';
  btnTransmision.style.display = 'none';
  btnTerminar.style.display = 'none';

  console.log('✅ Todo finalizado. Procesando...');

  if (mediaRecorder && grabando) {
    mediaRecorder.stop();
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

function actualizarBordeVideo() {
  video.classList.remove('borde-verde', 'borde-rojo');
  if (!camaraActiva) return;

  if (transmisionActiva) {
    video.classList.add('borde-verde');
  } else {
    video.classList.add('borde-rojo');
  }
}

function mostrarResultadoYBotonRefrescar(result = null) {
  resultadoDiv.style.display = 'block';
  resultadoDiv.innerHTML = '';

  const btnRefrescar = document.createElement('button');
  btnRefrescar.textContent = '🔄 Refrescar Página';
  btnRefrescar.classList.add('btn-refrescar');
  btnRefrescar.onclick = () => location.reload();

  if (procesamientoCompletado && result) {
    const resultadoTexto = document.createElement('p');
    resultadoTexto.textContent = '📊 Resultado del análisis recibido:';
    const info = document.createElement('p');
    info.textContent = `→ Archivo: ${result.filename} | Tamaño: ${result.size} bytes`;
    resultadoDiv.appendChild(resultadoTexto);
    resultadoDiv.appendChild(info);
  } else {
    const errorTexto = document.createElement('p');
    errorTexto.textContent = '⚠️ No se pudo obtener respuesta del análisis. Puedes refrescar la página manualmente.';
    resultadoDiv.appendChild(errorTexto);
  }

  resultadoDiv.appendChild(btnRefrescar);
}
