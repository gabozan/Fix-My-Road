// Se importan las librerías necesarias:
// - `@google-cloud/functions-framework`: para declarar funciones HTTP en Cloud Functions.
// - `express`: para manejar rutas HTTP de forma más estructurada.
// - `cors`: para permitir llamadas desde cualquier origen (CORS).
// - `@google-cloud/storage`: para interactuar con Cloud Storage.
const functions = require('@google-cloud/functions-framework');
const express = require('express');
const cors = require('cors');
const { Storage } = require('@google-cloud/storage');

// Se inicializa la app con CORS permitido para todos los orígenes.
// También se prepara el bucket donde se almacenarán los archivos.
const app = express();
app.use(cors({ origin: '*' }));

const storage = new Storage();
const bucket = storage.bucket('fixmyroad-videos');

// Antes de llegar a las rutas, se imprime por consola el método y la ruta de cada petición recibida.
// Útil para depuración y trazabilidad.
app.use((req, res, next) => {
  console.log('📥 Petición:', req.method, req.path);
  next();
});

// Esta ruta recibe archivos binarios de tipo video mediante POST.
// El nombre base del archivo se espera como parámetro en la query (`baseVideoName`).
// Guarda el archivo en el bucket con extensión `.webm`.
app.post(
  '/upload-video',
  express.raw({ type: 'video/*', limit: '512mb' }),
  async (req, res) => {
    const basename = req.query.baseVideoName;
    console.log('🧩 Nombre desde query (video):', basename);

    if (!req.body || !req.body.length || !basename) {
      return res
        .status(400)
        .json({ error: 'Faltan datos: vídeo o parámetro baseVideoName' });
    }

    const filename = `videos/${basename}.webm`;
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
  }
);

// Esta ruta recibe un JSON con un array de posiciones GPS y las guarda como archivo .json en el bucket.
// El nombre base del archivo también se recibe como parámetro en la query (`basePositionsName`).
app.post(
  '/upload-positions',
  express.json(),
  async (req, res) => {
    const basename = req.query.basePositionsName;
    console.log('🧩 Nombre desde query (positions):', basename);

    if (!Array.isArray(req.body) || !basename) {
      return res
        .status(400)
        .json({ error: 'Faltan datos: posiciones o parámetro basePositionsName' });
    }

    const filename = `positions/${basename}.json`;
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
  }
);

// Se expone la app de Express como una Cloud Function con el nombre `uploadVideo`.
functions.http('uploadVideo', app);