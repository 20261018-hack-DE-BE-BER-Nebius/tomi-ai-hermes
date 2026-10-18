#!/bin/sh
set -eu
# Hermes intentionally disallows wheel installs. Its supported development route is editable.
# Keep this checkout within the service's own ignored runtime directory.
revision=d923a5eb487a17c0a68801bba9ef0f56c81040a8
runtime=data/hermes-runtime
if [ ! -d "$runtime/.git" ]; then
  mkdir -p "$runtime"
  git -C "$runtime" init
  git -C "$runtime" remote add origin https://github.com/NousResearch/hermes-agent
fi
git -C "$runtime" fetch origin "$revision" --depth=1
git -C "$runtime" checkout --detach "$revision"
uv pip install --python .venv/bin/python --editable "$runtime"
