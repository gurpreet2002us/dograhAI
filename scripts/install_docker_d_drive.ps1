$ErrorActionPreference = "Stop"

# Check if running as Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warning "Please right-click this script or open an Administrator PowerShell to run this script."
    Read-Host "Press Enter to exit"
    exit 1
}

$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"

if (-not (Test-Path $installerPath)) {
    Write-Host "Downloading Docker Desktop Installer (this may take a minute)..."
    Invoke-WebRequest -Uri "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -OutFile $installerPath
}

Write-Host "Installing Docker Desktop to D:\Docker..."
Start-Process $installerPath -ArgumentList "install --quiet --accept-license --installation-dir=D:\Docker" -Wait -NoNewWindow

Write-Host "Docker Desktop installation complete!"
Write-Host "IMPORTANT NEXT STEPS:"
Write-Host "1. Open Docker Desktop from your Start Menu."
Write-Host "2. Accept any initial prompts and wait for the Docker Engine to fully start (green icon in bottom left)."
Write-Host "3. Once it's running, completely quit Docker Desktop (right click the whale icon in the system tray -> Quit Docker Desktop)."
Write-Host "4. Finally, run the 'move_docker_wsl_to_d.ps1' script to move the hidden container storage to D:."
Read-Host "Press Enter to exit"
