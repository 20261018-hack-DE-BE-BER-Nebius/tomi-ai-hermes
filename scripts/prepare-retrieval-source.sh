#!/bin/sh
set -eu
revision=88abda0d1882eb56a5cd78bc226f1fbc929cc33b
checkout=data/retrieval-source
if [ ! -d "$checkout/.git" ]; then
  mkdir -p "$checkout"
  git -C "$checkout" init
  git -C "$checkout" remote add origin https://github.com/october-18-hackathon/nemotron-agentic-ai-challenge
fi
git -C "$checkout" fetch origin "$revision" --depth=1
git -C "$checkout" checkout --detach "$revision"
printf '%s\n' "Pinned model-service source prepared at $checkout/infra/model-service. Review the Dockerfile and model terms before building."
