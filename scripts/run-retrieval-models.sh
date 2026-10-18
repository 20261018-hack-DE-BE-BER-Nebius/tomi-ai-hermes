#!/bin/sh
set -eu
# Use on the assigned Linux GPU VM. Managed endpoints instead run this image directly on port 8000.
: "${TOMI_RETRIEVAL_IMAGE:?Set the reviewed local tag or organizer-provided immutable image digest}"
docker run --rm --name tomi-nemotron-models --gpus device=0 \
  --read-only --tmpfs /tmp:rw,nosuid,nodev,size=1g \
  --cap-drop ALL --security-opt no-new-privileges \
  -p 127.0.0.1:8000:8000 "$TOMI_RETRIEVAL_IMAGE"
