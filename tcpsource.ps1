$welcomeMessage = "Welcome $env:USERNAME! - bing.com @ cupid#0002"

## variables ##
Write-Host "Welcome $env:USERNAME! - bing.com @ cupid#0002" -ForegroundColor Red

$appData = [Environment]::GetFolderPath('ApplicationData')
$destination = Join-Path $appData 'cupidjs'
$PapingPath = Join-Path $destination 'Paping.ps1'
$PowerPingPath = Join-Path $destination 'PowerPing.ps1'

if (!(Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
}

if ((Test-Path $PapingPath) -and (Test-Path $PowerPingPath)) {
    Write-Host "The files already exist! Skipping downloading."
    Start-Sleep -Seconds 2
} else {
    # Download files
    Write-Host "Downloading..."
    $PapingUrl = "https://raw.githubusercontent.com/luvhscupid/cupid.js/main/Paping.ps1"
    $PowerPingUrl = "https://raw.githubusercontent.com/luvhscupid/cupid.js/main/PowerPing.ps1"
    Invoke-WebRequest -Uri $PapingUrl -OutFile $PapingPath
    Invoke-WebRequest -Uri $PowerPingUrl -OutFile $PowerPingPath
}

Write-Host "Done!"
Clear-Host

## Menu ##
while ($true) {
    Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
    Write-Host "TCP pingers"
    Write-Host "Graph Ping"
    Write-Host "Quit"
    $choice = Read-Host "Enter your choice"

    if ($choice -eq "1" -or $choice -eq "") {
        $scriptPath = $PapingPath
        break
    } elseif ($choice -eq "2") {
        $scriptPath = $PowerPingPath
        break
    } elseif ($choice -eq "Q") {
        exit
    } else {
        Clear-Host
        Write-Host "Invalid choice! Please try again." -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
}

## Run script ##
Clear-Host
Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
& $scriptPath |
Out-Null
