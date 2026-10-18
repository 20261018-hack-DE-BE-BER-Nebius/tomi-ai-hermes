#!/bin/sh
set -eu
# Run on a Linux amd64 builder with at least 60 GB free disk, not an Apple GPU runtime.
checkout=data/retrieval-source
expected=88abda0d1882eb56a5cd78bc226f1fbc929cc33b
actual=$(git -C "$checkout" rev-parse HEAD)
[ "$actual" = "$expected" ] || { printf '%s\n' 'Unexpected organizer source revision'; exit 1; }
docker buildx build --platform linux/amd64 --load -t nemotron-challenge-models:local "$checkout/infra/model-service"
