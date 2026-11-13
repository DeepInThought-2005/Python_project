#!/bin/sh
# Build Flappy Bird and ChessL for the browser with pygbag (Pygame on WebAssembly).
# Usage: web/build.sh <output dir>   e.g. web/build.sh ../website/public/games
# Needs: pip install pygbag
set -eu
out=$(cd "$1" && pwd)
root=$(cd "$(dirname "$0")/.." && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

# Only the code and images each game uses (no __pycache__ or scratch files).
mkdir -p "$stage/flappybird/imgs" "$stage/chessl/Image/Boards" "$stage/chessl/Image/Pieces"
cp "$root"/flappybird/*.py "$stage/flappybird/"
cp "$root"/flappybird/imgs/*.png "$stage/flappybird/imgs/"
cp "$root"/ChessL/*.py "$stage/chessl/"
cp "$root/ChessL/Image/Boards/blue.png" "$stage/chessl/Image/Boards/"
cp -R "$root/ChessL/Image/Pieces/Staunty" "$stage/chessl/Image/Pieces/"

for game in flappybird chessl; do
  python -m pygbag --build --title "$game" "$stage/$game" >/dev/null
  mkdir -p "$out/$game"
  web="$stage/$game/build/web"
  cp "$web/index.html" "$web/$game.apk" "$web/$game.tar.gz" "$web/favicon.png" "$out/$game/"
  # Let the game use the whole page instead of half its width.
  sed -i.bak 's/gui_divider : 2,/gui_divider : 1,/' "$out/$game/index.html" && rm "$out/$game/index.html.bak"
  echo "built $out/$game"
done
