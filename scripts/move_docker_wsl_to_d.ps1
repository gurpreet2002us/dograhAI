$ErrorActionPreference = "Stop"

Write-Host "Ensuring Docker is stopped..."
Stop-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "Shutting down WSL to release locks..."
wsl --shutdown
Start-Sleep -Seconds 3

$targetDir = "D:\DockerData\wsl"
New-Item -ItemType Directory -Force -Path "$targetDir\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$targetDir\distro" | Out-Null

$rawDistros = wsl --list --quiet
$distros = $rawDistros -replace '\x00', '' -split '\r?\n' | Where-Object { $_ -match '\S' }

$expectedDistros = @("docker-desktop", "docker-desktop-data")
$foundAny = $false

foreach ($distro in $expectedDistros) {
    if ($distros -contains $distro) {
        $foundAny = $true
        Write-Host "Processing $distro..."
        
        $subFolder = if ($distro -eq "docker-desktop") { "distro" } else { "data" }
        $tarFile = "$targetDir\$distro.tar"
        
        Write-Host "  -> Exporting $distro..."
        wsl --export $distro $tarFile
        
        Write-Host "  -> Unregistering original $distro from C: drive..."
        wsl --unregister $distro
        
        Write-Host "  -> Importing $distro into D: drive..."
        wsl --import $distro "$targetDir\$subFolder" $tarFile --version 2
        
        Write-Host "  -> Cleaning up temporary tar file..."
        Remove-Item $tarFile
    } else {
        Write-Host "Skipping $distro (not found on system, this is normal depending on your Docker version)."
    }
}

if (-not $foundAny) {
    Write-Error "No Docker WSL distros found! Did you start Docker Desktop at least once after installing?"
    exit 1
}

Write-Host "======================================="
Write-Host "Success! Docker WSL data has been completely moved to $targetDir."
Write-Host "You can now start Docker Desktop from your Start Menu!"
Write-Host "After Docker is running, you can run '.\scripts\start_docker_detached.ps1' to start Dograh."
Read-Host "Press Enter to exit"
