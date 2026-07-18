# PowerShell wrapper for read-only M0 environment diagnostics.
if (-not $env:CARGO_TARGET_DIR) {
    $env:CARGO_TARGET_DIR = Join-Path ([System.IO.Path]::GetTempPath()) "turing-doctor-target"
}

& cargo run --locked -p xtask -- doctor @args
exit $LASTEXITCODE
