// Se importan las herramientas necesarias:
// - `functions-framework`: para definir una Cloud Function HTTP en Google Cloud.
// - `express`: para manejar rutas y peticiones de forma estructurada.
// - `cors`: para permitir el acceso desde otros orígenes (CORS).
// - `Storage`: para trabajar con Google Cloud Storage (subida de archivos).
const functions = require('@google-cloud/functions-framework');
const express = require('express');
const cors = require('cors');
const { Storage } = require('@google-cloud/storage');

// Se crea la app Express y se permite CORS desde cualquier origen.
// Se instancia el cliente de almacenamiento y se selecciona el bucket deseado.
const app = express();
app.use(cors({ origin: '*' }));

const storage = new Storage();
const bucket = storage.bucket('fixmyroad-videos');

// Se imprime por consola cada petición HTTP que llega a la función.
// Esto ayuda a rastrear la actividad y detectar errores.
app.use((req, res, next) => {
  console.log('📥 Petición:', req.method, req.path);
  next();
});

// Esta ruta recibe un archivo de vídeo en el cuerpo de la petición (binario).
// Si todo está correcto, lo guarda en el bucket bajo la carpeta `videos/`
// con un nombre generado automáticamente usando la fecha/hora actual.
app.post('/upload-video', express.raw({ type: 'video/*', limit: '512mb' }), async (req, res) => {
  if (!req.body || !req.body.length) {
    return res.status(400).json({ error: 'No llegó ningún vídeo' });
  }

  const filename = `videos/${Date.now()}_video.webm`;
  const file = bucket.file(filename);

  try {
    await file.save(req.body, {
      metadata: { contentType: req.headers['content-type'] },
      resumable: false
    });
    console.log(`✅ Subido vídeo: ${filename}`);
    res.json({ ok: true, filename });
  } catch (err) {
    console.error('❌ Error subiendo vídeo:', err);
    res.status(500).json({ error: 'Error subiendo vídeo' });
  }
});

// Esta ruta recibe un array JSON de posiciones GPS.
// Lo guarda en el bucket en la carpeta `positions/` con un nombre
// automático basado en la hora del servidor.
app.post('/upload-positions', express.json(), async (req, res) => {
  if (!Array.isArray(req.body)) {
    return res.status(400).json({ error: 'Formato inválido de posiciones' });
  }

  const filename = `positions/${Date.now()}_positions.json`;
  const file = bucket.file(filename);

  try {
    await file.save(JSON.stringify(req.body, null, 2), {
      metadata: { contentType: 'application/json' },
      resumable: false
    });
    console.log(`✅ Subidas posiciones: ${filename}`);
    res.json({ ok: true, filename });
  } catch (err) {
    console.error('❌ Error subiendo posiciones:', err);
    res.status(500).json({ error: 'Error subiendo posiciones' });
  }
});

// Se exporta la aplicación Express como una función HTTP para ser usada en Cloud Functions.
// El nombre registrado será `uploadVideo`, aunque ahora maneja dos rutas: videos y posiciones.
functions.http('uploadVideo', app);
