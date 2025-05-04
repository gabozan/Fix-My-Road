const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const speech = require('@google-cloud/speech');
const app = express();
const port = 3000;
const upload = multer({ dest: 'uploads/' });
const client = new speech.SpeechClient({
  keyFilename: 'fixmyroad-458407-264842d5b72a.json'
});

app.post('/transcribe', upload.single('audio'), async (req, res) => {
  try {
    const filePath = req.file.path;

    const file = fs.readFileSync(filePath);
    const audioBytes = file.toString('base64');

    const audio = {
      content: audioBytes,
    };

    const config = {
      encoding: 'WEBM_OPUS',
      sampleRateHertz: 48000,
      languageCode: 'es-ES'
    };

    const request = {
      audio: audio,
      config: config,
    };

    const [response] = await client.recognize(request);
    const transcription = response.results
      .map(result => result.alternatives[0].transcript)
      .join('\n');
    fs.unlinkSync(filePath);

    res.json({ text: transcription });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error en la transcripción' });
  }
});

app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
