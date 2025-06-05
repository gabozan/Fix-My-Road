# Funcions Cloud de Fix My Road

Aquest document recull el codi de les funcions Cloud utilitzades al projecte i explica breument com funcionen i com es poden cridar. Els fitxers `record_function.js` i `trigger_yolo_function.js` contenen el codi complet.

## Què són les Cloud Functions?

Les Google Cloud Functions permeten executar fragments de codi en resposta a peticions HTTP o esdeveniments sense haver de gestionar cap servidor. S'escalen automàticament i es despleguen de forma senzilla.

## Funció `uploadVideo`

Es troba a `multimedia_system/public_html/record/index.js` i es pot veure íntegra a `docs/record_function.js`. Defineix dues rutes HTTP:

- `POST /upload-video`: rep un vídeo i el desa al bucket `fixmyroad-videos` dins de la carpeta `videos/` amb el nom indicat al paràmetre `baseVideoName`.
- `POST /upload-positions`: rep un JSON amb coordenades i el desa a `positions/` amb el nom indicat al paràmetre `basePositionsName`.

S'exposa com a Cloud Function HTTP sota el nom `uploadVideo`.

### Invocació

Una vegada desplegada, es pot cridar via peticions HTTP. Per exemple:

```bash
curl -X POST "https://REGIO-PROJECTID.cloudfunctions.net/uploadVideo/upload-video?baseVideoName=123" \
     --data-binary @video.webm \
     -H "Content-Type: video/webm"
```

## Funció `processVideo`

Ubicada a `multimedia_system/public_html/yolo/triggerYolo/index.js` (també copiada a `docs/trigger_yolo_function.js`). S'activa automàticament quan es puja un arxiu a `videos/` en el bucket. Envia la informació a un servei de Cloud Run perquè processi el vídeo amb YOLO.

### Invocació

No es crida manualment. Cada cop que es puja un vídeo al bucket, Google Cloud Storage genera un esdeveniment *Object Finalize* que executa aquesta funció.

