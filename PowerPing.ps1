## variables ##
Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red

$fileUrl = "https://github.com/Killeroo/PowerPing/releases/download/v1.3.3/PowerPing.exe"
$destination = Join-Path ([Environment]::GetFolderPath('ApplicationData')) 'cupidjs\src'

if (Test-Path (Join-Path $destination 'PowerPing.exe')) {
    Clear-Host
    Write-Host "The file already exists! Stopping downloading."
    Start-Sleep -Seconds 1
    # Download file
    Clear-Host
    Write-Host "Downloading..."
    Invoke-WebRequest -Uri $fileUrl -OutFile (Join-Path $destination 'PowerPing.exe')
}

Write-Host "Done!"


## Expected Jobs ##
while ($true) {
    Clear-Host
    Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
    Write-Host "IP OR WEBSITE: " -NoNewline -ForegroundColor Green
    $IP = Read-Host
    if ([string]::IsNullOrEmpty($IP)) {
        Clear-Host
        Write-Host "You must enter something!" -ForegroundColor Red
        Start-Sleep -Seconds 1
    } elseif (!(Test-Connection -ComputerName $IP -Count 2 -Quiet)) {
        Clear-Host
        Write-Host "Invalid IP or Website!" -ForegroundColor Red
        Start-Sleep -Seconds 1
    } else {
        break
    }
}

## the actual Jobs ##
Clear-Host
Push-Location $destination
Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
& ".\PowerPing.exe" --cg $IP

Pop-Location
