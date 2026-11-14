#!/usr/bin/env bash
# Usage: tools/make_reel_from_cards.sh posts/<folder> [seconds_per_card]
# Builds a 1080x1920 Reel (cardN.jpg centered on #0C0F12, crossfades) -> <folder>/reel.mp4
set -e
DIR="$1"; S="${2:-3}"; F=0.4
cards=($(ls "$DIR"/card*.jpg | sort -V)); n=${#cards[@]}
inputs=""; filt=""
for i in "${!cards[@]}"; do
  inputs+=" -loop 1 -t $S -i ${cards[$i]}"
  filt+="[$i:v]scale=1080:1350,pad=1080:1920:0:285:color=0x0C0F12,setsar=1,fps=30,format=yuv420p[v$i];"
done
prev="v0"; off=0
for ((i=1;i<n;i++)); do
  off=$(echo "$off + $S - $F" | bc)
  filt+="[$prev][v$i]xfade=transition=slideleft:duration=$F:offset=$off[x$i];"; prev="x$i"
done
total=$(echo "$S*$n - $F*($n-1)" | bc)
ffmpeg -y -loglevel error $inputs -f lavfi -t $total -i anullsrc=r=44100:cl=stereo \
  -filter_complex "${filt%;}" -map "[$prev]" -map $n:a -c:v libx264 -preset slow -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart "$DIR/reel.mp4"
