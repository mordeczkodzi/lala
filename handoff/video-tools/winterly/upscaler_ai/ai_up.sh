#!/usr/bin/env bash
# ai_up.sh klip start dlugosc -> klip_ai.mp4 (ESRGAN x3 -> 1080x1920 + lekkie CAS)
set -e; n=$1; st=$2; d=$3
ffmpeg -nostdin -v error -ss $st -t $d -i $n.mp4 -an -f rawvideo -pix_fmt rgb24 - \
 | node ../upjs/up.js 480 854 3 slim 2>$n.log \
 | ffmpeg -nostdin -v error -y -f rawvideo -pix_fmt rgb24 -s 1440x2562 -r 24 -i - -vf "scale=1080:1920:flags=lanczos,cas=0.35,fps=30" -c:v libx264 -crf 14 -preset medium ${n}_ai.mp4
echo "gotowe $n"
