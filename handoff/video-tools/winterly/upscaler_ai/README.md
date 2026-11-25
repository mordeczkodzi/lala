# Upscaler AI (ESRGAN-slim, offline, CPU)

Do klipów z Higgsfield w 480p. Daje ostrzejsze diody i mniej „schodków” niż zwykłe powiększanie.

Instalacja (raz, w tym folderze):
    npm init -y && npm install @tensorflow/tfjs@4.11.0 @tensorflow/tfjs-backend-wasm@4.11.0 @upscalerjs/esrgan-slim

Użycie (fragment klipu -> klip_ai.mp4, 1080x1920):
    ./ai_up.sh klip START DŁUGOŚĆ      # np. ./ai_up.sh k6 0.0 4.75
Ok. 9 s na klatkę na 1 rdzeń, więc puszczaj kilka klipów równolegle i przerabiaj tylko fragmenty używane w montażu.
W ai_up.sh popraw ścieżkę do up.js, jeśli uruchamiasz z innego folderu.
