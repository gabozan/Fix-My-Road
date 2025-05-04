const functions = require('@google-cloud/functions-framework');
const express   = require('express');
const cors      = require('cors');
const { Storage } = require('@google-cloud/storage');

const app = express();
app.use(cors({ origin: '*' }));

const storage = new Storage();
const bucket = storage.bucket('fixmyroad-videos');

app.post('/', express.raw({ type: 'video/*', limit: '512mb' }), async (req, res) => {
  if (!req.body || !req.body.length) {
    return res.status(400).json({ error: 'No llegó ningún dato' });
  }

  const userId = 'alice';
  const filename = `videos/${Date.now()}_${userId}.webm`;
  const file = bucket.file(filename);  

  try {
    await file.save(req.body, {
      metadata: { contentType: req.headers['content-type'] },
      resumable: false
    });
    console.log(`✅ Subido ${filename} (${req.body.length} bytes)`);
    return res.json({ ok: true, filename, size: req.body.length });
  } catch (err) {
    console.error('❌ Error subiendo a Storage:', err);
    return res.status(500).json({ error: 'Fallo al subir a Cloud Storage' });
  }
});

functions.http('uploadVideo', app);
