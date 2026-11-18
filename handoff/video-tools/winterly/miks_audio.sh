#!/usr/bin/env bash
# Miks dźwięku do reklamy Winterly i sklejenie z obrazem.
# Użycie: bash miks_audio.sh lektor.mp3 muzyka.mp3 obraz.mp4 GOTOWY_FILM.mp4
#
# Ustawienia wypracowane z właścicielem (po uwagach „głos sztuczny”, „muzyka pompuje”, „za głośno”):
#  - głos BEZ odszumiania (afftdn robił sztuczny głos), lekki EQ + kompresja, ok. -15 LUFS,
#  - muzyka równo, cicho (ok. -34 LUFS), BEZ ściszania pod głos (ducking „pompował”),
#    na planszy końcowej (ostatnie ~2,3 s) muzyka trochę głośniej,
#  - całość ok. -14 LUFS, limiter z level=0 (bez automatycznego podgłaśniania do 0 dB).
set -euo pipefail
VOICE="$1"; MUSIC="$2"; VIDEO="$3"; OUT="$4"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
VEND=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")
TMP=$(mktemp -d)
LOUD=$(python3 -c "print(f'{float(\"$VEND\")+0.1:.2f}')")
FADE=$(python3 -c "print(f'{float(\"$D\")-1.2:.2f}')")

ffmpeg -nostdin -v error -y -i "$VOICE" -af "highpass=f=70,equalizer=f=200:t=q:w=1:g=2,equalizer=f=6500:t=q:w=1.2:g=-2.5,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=200:makeup=1.5,loudnorm=I=-15:TP=-2:LRA=7" -ar 48000 "$TMP/v.wav"
ffmpeg -nostdin -v error -y -i "$MUSIC" -t "$D" -af "acompressor=threshold=-24dB:ratio=3:attack=20:release=300,loudnorm=I=-34:TP=-9:LRA=6,volume='if(gt(t,$LOUD),1.7,1)':eval=frame,afade=t=in:d=0.3,afade=t=out:st=$FADE:d=1.2" -ar 48000 "$TMP/m.wav"
ffmpeg -nostdin -v error -y -i "$TMP/v.wav" -i "$TMP/m.wav" -filter_complex "[0:a]apad=whole_dur=$D[v];[v][1:a]amix=inputs=2:normalize=0:duration=longest,volume=1.5dB,alimiter=limit=0.8:level=0,atrim=0:$D[a]" -map "[a]" -ar 48000 "$TMP/mix.wav"
ffmpeg -nostdin -v error -y -i "$VIDEO" -i "$TMP/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "OK $OUT"
ffmpeg -nostdin -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
echo "(cel: I ok. -14 LUFS, Peak poniżej -1 dBFS; jeśli I jest za niskie, zwiększ volume=1.5dB w trzecim kroku)"
