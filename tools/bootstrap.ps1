# PowerShell wrapper for the M0 bootstrap entry point.
if (-not $env:CARGO_TARGET_DIR) {
    $env:CARGO_TARGET_DIR = Join-Path ([System.IO.Path]::GetTempPath()) "turing-bootstrap-target"
}

& cargo run --locked -p xtask -- bootstrap @args
exit $LASTEXITCODE
