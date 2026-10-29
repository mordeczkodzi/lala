#!/usr/bin/env bash
# Tnie klipy z generatora (Gemini Omni / Veo) na równe kawałki 1080x1920, 30 fps, bez dźwięku,
# i skleja je w jeden plik joined.mp4.
#
# Użycie:  ./cut.sh <katalog_wyjściowy> <plik_listy>
# Plik listy: jedna linia na ujęcie -> "ścieżka_do_klipu  start_s  długość_s"
#   /uploads/klip_lozko.mp4   0.3  3.5
#   /uploads/klip_park.mp4    3.6  2.6
set -euo pipefail
out=$1; list=$2
mkdir -p "$out"; : > "$out/list.txt"
i=0
while read -r line; do
  line="${line%%#*}"                      # komentarze po # są pomijane
  read -r src start len <<< "$line" || true
  [[ -z "${src:-}" ]] && continue
  i=$((i+1)); name=$(printf 'c%02d.mp4' "$i")
  ffmpeg -nostdin -v error -y -ss "$start" -i "$src" -t "$len" -an \
    -vf "scale=1080:1920,fps=30,setsar=1" -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p "$out/$name"
  echo "file '$name'" >> "$out/list.txt"
done < "$list"
(cd "$out" && ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy joined.mp4)
ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/joined.mp4"
