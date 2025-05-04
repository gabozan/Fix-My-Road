const video = document.getElementById('video');
const btnCamara = document.getElementById('toggleCamara');
const btnTransmision = document.getElementById('toggleTransmision');
const btnTerminar = document.getElementById('terminarTodo');
const realtimeContainer = document.getElementById('realtime-container');

let stream = null;
let camaraActiva = false;
let transmisionActiva = false;
let procesamientoCompletado = false; // Simulación

// Crear contenedor para resultado justo después del contenedor de cámara
const resultadoDiv = document.createElement('div');
resultadoDiv.id = 'resultado-procesamiento';
resultadoDiv.classList.add('resultado-procesamiento');
resultadoDiv.style.display = 'none'; // Inicialmente oculto
realtimeContainer.insertAdjacentElement('afterend', resultadoDiv);

btnCamara.addEventListener('click', () => {
  if (!camaraActiva) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((s) => {
        stream = s;
        video.srcObject = stream;
        camaraActiva = true;
        btnCamara.textContent = 'Cerrar Cámara';
        btnTransmision.disabled = false;
        btnTerminar.disabled = false;
      })
      .catch(err => {
        console.error('Error al abrir la cámara:', err);
      });
  } else {
    cerrarCamara();
  }
});

btnTransmision.addEventListener('click', () => {
  transmisionActiva = !transmisionActiva;
  actualizarBordeVideo();

  btnTransmision.textContent = transmisionActiva
    ? 'Pausar Transmisión'
    : 'Iniciar Transmisión';

  console.log(transmisionActiva
    ? '📡 Transmisión activa...'
    : '⛔ Transmisión pausada');
});

btnTerminar.addEventListener('click', () => {
  cerrarCamara();
  transmisionActiva = false;
  actualizarBordeVideo();

  // Desactiva y oculta los botones
  btnCamara.style.display = 'none';
  btnTransmision.style.display = 'none';
  btnTerminar.style.display = 'none';

  console.log('✅ Todo finalizado. Procesando...');

  // Simula una llamada a API (1s)
  setTimeout(() => {
    procesamientoCompletado = Math.random() > 0.3; // 70% éxito
    mostrarResultadoYBotonRefrescar();
  }, 1000);
});

function cerrarCamara() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    stream = null;
  }
  camaraActiva = false;
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

function mostrarResultadoYBotonRefrescar() {
  // Muestra el div de resultado solo cuando el procesamiento se complete
  resultadoDiv.style.display = 'block'; // Mostrar el resultado
  resultadoDiv.innerHTML = ''; // Limpia contenido anterior si lo hay

  const btnRefrescar = document.createElement('button');
  btnRefrescar.textContent = '🔄 Refrescar Página';
  btnRefrescar.classList.add('btn-refrescar');
  btnRefrescar.onclick = () => location.reload();

  if (procesamientoCompletado) {
    const resultadoTexto = document.createElement('p');
    resultadoTexto.textContent = '📊 Resultado del análisis recibido:';
    const info = document.createElement('p');
    info.textContent = '→ Número de baches: [en espera] | Tipo: [en espera]';
    resultadoDiv.appendChild(resultadoTexto);
    resultadoDiv.appendChild(info);
  } else {
    const errorTexto = document.createElement('p');
    errorTexto.textContent = '⚠️ No se pudo obtener respuesta del análisis. Puedes refrescar la página manualmente.';
    resultadoDiv.appendChild(errorTexto);
  }

  resultadoDiv.appendChild(btnRefrescar);
}
