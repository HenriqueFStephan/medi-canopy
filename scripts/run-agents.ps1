param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("news", "research", "all")]
    [string]$Agent,

    [switch]$DryRun
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$args = @("-m", "agents.run", "--agent", $Agent)
if ($DryRun) { $args += "--dry-run" }

Write-Host "Running CanaHub agent: $Agent" -ForegroundColor Green

$venvPython = Join-Path $Root "backend\.venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython @args
} else {
    python @args
}
