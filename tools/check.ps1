# PowerShell wrapper for the complete local M0 repository check.
if (-not $env:CARGO_TARGET_DIR) {
    $env:CARGO_TARGET_DIR = Join-Path ([System.IO.Path]::GetTempPath()) "turing-check-target"
}

& cargo run --locked -p xtask -- check @args
exit $LASTEXITCODE
