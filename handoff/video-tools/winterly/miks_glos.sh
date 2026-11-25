#!/usr/bin/env bash
# Miks lektora BEZ "pompowania": stałe podbicie głośności zamiast automatycznej regulacji (loudnorm w trybie dynamicznym
# podbijał szum w pauzach i co chwilę zmieniał głośność – stąd „dziwne dźwięki”).
# Użycie: bash miks_glos.sh lektor.wav obraz.mp4 GOTOWY.mp4 [muzyka.mp3]
#   muzyka opcjonalna: bardzo cicho (ok. -32 LUFS), stała głośność, wyciszenie na końcu.
set -euo pipefail
VOICE="$1"; VIDEO="$2"; OUT="$3"; MUSIC="${4:-}"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
TMP=$(mktemp -d)
# 1) barwa + łagodna kompresja (bez odszumiania – afftdn robił sztuczny głos)
ffmpeg -nostdin -v error -y -i "$VOICE" -af "highpass=f=70,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.2:g=-2,acompressor=threshold=-22dB:ratio=2:attack=20:release=250:makeup=1" -ar 48000 -ac 1 "$TMP/v1.wav"
# 2) pomiar i STAŁE podbicie do ok. -15 LUFS, potem tylko ogranicznik szczytów
I=$(ffmpeg -nostdin -i "$TMP/v1.wav" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-15.0-float('$I'),2))")
ffmpeg -nostdin -v error -y -i "$TMP/v1.wav" -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=60:level=0,apad=whole_dur=$D" -t "$D" -ar 48000 "$TMP/v.wav"
if [ -n "$MUSIC" ]; then
  MI=$(ffmpeg -nostdin -i "$MUSIC" -t "$D" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
  MG=$(python3 -c "print(round(-32.0-float('$MI'),2))"); F=$(python3 -c "print(f'{float(\"$D\")-1.2:.2f}')")
  ffmpeg -nostdin -v error -y -i "$MUSIC" -t "$D" -af "volume=${MG}dB,afade=t=in:d=0.3,afade=t=out:st=$F:d=1.2" -ar 48000 -ac 1 "$TMP/m.wav"
  ffmpeg -nostdin -v error -y -i "$TMP/v.wav" -i "$TMP/m.wav" -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.86:level=0" -ar 48000 "$TMP/mix.wav"
else
  cp "$TMP/v.wav" "$TMP/mix.wav"
fi
ffmpeg -nostdin -v error -y -i "$VIDEO" -i "$TMP/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "OK $OUT (podbicie głosu: ${G} dB)"
ffmpeg -nostdin -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
