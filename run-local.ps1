$ErrorActionPreference = "Stop"

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
  Copy-Item ".env.example" ".env"
}

if (Test-Path ".env") {
  Get-Content ".env" | ForEach-Object {
    if ($_ -match '^(?<key>[A-Za-z_][A-Za-z0-9_]*)=(?<value>.*)$') {
      $name = $Matches['key']
      $value = $Matches['value']
      if (-not [string]::IsNullOrWhiteSpace($name)) {
        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
      }
    }
  }
}

function Test-Command {
  param([string]$Cmd)
  try {
    $null = Get-Command $Cmd -ErrorAction Stop
    return $true
  } catch {
    return $false
  }
}

if (Test-Command "docker") {
  $composeCheck = & docker compose version 2>$null
  if ($LASTEXITCODE -eq 0) {
    $composeCmd = "docker compose"
  } else {
    if (Test-Command "docker-compose") {
      $composeCmd = "docker-compose"
    } else {
      Write-Host "Docker Compose not found. Install Docker Desktop and try again."
      exit 1
    }
  }
} else {
  Write-Host "Docker not found. Install Docker Desktop and try again."
  exit 1
}

& $composeCmd split(' ') up -d --build

$appPort = if ($env:APP_PORT) { $env:APP_PORT } else { "3000" }
$apiPort = if ($env:API_PORT) { $env:API_PORT } else { "8000" }

Write-Host "PromptForge is running:"
Write-Host "Frontend: http://localhost:$appPort"
Write-Host "Backend Docs: http://localhost:$apiPort/docs"
