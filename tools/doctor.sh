#!/usr/bin/env sh
set -eu

export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/turing-doctor-target}"
exec cargo run --locked -p xtask -- doctor "$@"
