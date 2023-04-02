$currentVer = $null
$response = $false
$localVer = 4.0

$appData = [Environment]::GetFolderPath('ApplicationData')

$cupidjsPath = Join-Path $appData 'cupidjs'

if (-not (Test-Path $cupidjsPath)) {
    New-Item -ItemType Directory -Path $cupidjsPath | Out-Null
}

if (-not $MyInvocation.MyCommand.Path) {
    $scriptPath = Join-Path $cupidjsPath 'tcpsource.ps1'
} else {
    $scriptPath = $MyInvocation.MyCommand.Path
}

Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luvhscupid/cupid.js/main/checkversion' -UseBasicParsing | ForEach-Object {
    $currentVer = $_.Content.Trim()
    $response = $true
}

if ($localVer -ne $currentVer) {
    Write-Host "New CupidJS version is available, updating the script..."

    Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luvhscupid/cupid.js/main/tcpsource.ps1' -UseBasicParsing | ForEach-Object {
        $code = $_.Content
        Set-Content -Path $scriptPath -Value $code
    }

    Write-Host "Successfully updated CupidJS. Restarting Script... :)"
    Start-Sleep -Seconds 2
    & $scriptPath

    Write-Host "CupidJS has been updated!"
    & $scriptPath
    
## variables ##
$zipPath = Join-Path $env:USERPROFILE "paping_1.5.5_x86_windows.zip"
$fileUrl = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/paping/paping_1.5.5_x86_windows.zip"
$destination = $env:USERPROFILE 
$extractedFilePath = Join-Path $destination "paping.exe"
$newFileName = "tcp.exe"

Write-Host "Welcome $env:USERNAME! - bing.com @ cupid#0002" -ForegroundColor Red
Write-Host "Checking files..."
Start-Sleep -Seconds 1
if (Test-Path (Join-Path $destination $newFileName)) {
    Clear-Host
    Write-Host "The files already exists! , stopping downloading."
    Start-Sleep -Seconds 1
} else {
    Clear-Host
    Write-Host "Downloading..."
    Invoke-WebRequest -Uri $fileUrl -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $destination
    Rename-Item -Path $extractedFilePath -NewName $newFileName
    Remove-Item -Path $zipPath
    Remove-Item -Path $extractedFilePath
}

## Expected Jobs ##
while ($true) {
    Clear-Host
    Write-Host "Welcome $env:USERNAME! - bing.com @ cupid#0002" -ForegroundColor Red
    Write-Host "IP OR WEBSITE: " -NoNewline -ForegroundColor Green
    $IP = Read-Host
    if ([string]::IsNullOrEmpty($IP)) {
        Clear-Host
        Write-Host "You must enter something!" -ForegroundColor Red
        Start-Sleep -Seconds 1
    } elseif (!(Test-Connection -ComputerName $IP -Count 3 -Quiet)) {
        Clear-Host
        Write-Host "Invalid IP or Website!" -ForegroundColor Red
        Start-Sleep -Seconds 1
    } else {
        break
    }
}

while ($true) {
    Clear-Host
    Write-Host "Welcome $env:USERNAME! - bing.com @ cupid#0002" -ForegroundColor Red
    Write-Host "IP OR WEBSITE: $IP" -ForegroundColor Green
    Write-Host "PORTS: " -NoNewline -ForegroundColor Green
    $PORT = Read-Host
    if ([string]::IsNullOrEmpty($PORT)) {
        Clear-Host
        $PORT = 443
        break
    } elseif ($PORT -notmatch '^\d+$' -or [int]$PORT -lt 1 -or [int]$PORT -gt 65535) {
        Clear-Host
        Write-Host "Invalid Port number!" -ForegroundColor Red
        Start-Sleep -Seconds 2
    } else {
        break
    }
}

## the actual Jobs ##
Clear-Host
Push-Location $destination
Write-Host "Welcome $env:USERNAME! - bing.com @ cupid#0002" -ForegroundColor Red
& "$destination\tcp.exe" $IP -p $PORT | Select-String "^Connected" | ForEach-Object { $_ -replace "time=", "ping=" } | ForEach-Object { Write-Host $_ -ForegroundColor Green }
Pop-Location


} else {
    Write-Host "CupidJS is already up to date."
}
