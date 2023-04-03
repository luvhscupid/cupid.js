## variables ##
$zipPath = Join-Path $env:USERPROFILE "paping_1.5.5_x86_windows.zip"
$fileUrl = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/paping/paping_1.5.5_x86_windows.zip"
$destination = $env:USERPROFILE 
$extractedFilePath = Join-Path $destination "paping.exe"
$newFileName = "tcp.exe"

Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
Write-Host "Checking files..."
Start-Sleep -Seconds 1
if (Test-Path (Join-Path $destination $newFileName)) {
    Clear-Host
    Write-Host "The files already exists! , stopping downloading."
    Start-Sleep -Seconds 2
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
    Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
    Write-Host "IP OR WEBSITE: " -NoNewline -ForegroundColor Green
    $IP = Read-Host
    if ([string]::IsNullOrEmpty($IP)) {
        Clear-Host
        Write-Host "You must enter something!" -ForegroundColor Red
        Start-Sleep -Seconds 2
    } elseif (!(Test-Connection -ComputerName $IP -Count 3 -Quiet)) {
        Clear-Host
        Write-Host "Invalid IP or Website!" -ForegroundColor Red
        Start-Sleep -Seconds 2
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
Write-Host "Welcome $env:USERNAME! - bing.com @ CupidJS" -ForegroundColor Red
& "$destination\tcp.exe" $IP -p $PORT | Select-String "^Connected" | ForEach-Object { $_ -replace "time=", "ping=" } | ForEach-Object { Write-Host $_ -ForegroundColor Green }
Pop-Location

