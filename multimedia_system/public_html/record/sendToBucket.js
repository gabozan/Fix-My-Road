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

functions.http('uploadVideo', app);
