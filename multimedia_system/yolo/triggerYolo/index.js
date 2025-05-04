const functions = require('@google-cloud/functions-framework');
const fetch     = require('node-fetch');

functions.cloudEvent('processVideo', async (cloudEvent) => {
  const { bucket, name } = cloudEvent.data;
  if (!name.startsWith('videos/')) return;

  const filename = name.split('/').pop(); 
  const userIdMatch = filename.match(/^\d+_([^\.]+)\.webm$/);
  if (!userIdMatch) return; 
  const userId = userIdMatch[1];

  await fetch('https://yolo-processor-322599195853.europe-southwest1.run.app/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bucket, name, userId })
  });
});
