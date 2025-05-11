const functions = require('@google-cloud/functions-framework');
const express = require('express');
const cors = require('cors');
const { Storage } = require('@google-cloud/storage');

const app = express();
app.use(cors({ origin: '*' }));

const storage = new Storage();
const bucket = storage.bucket('fixmyroad-videos');

app.use((req, res, next) => {
  console.log('📥 Petición:', req.method, req.path);
  next();
});

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

functions.http('uploadVideo', app);
