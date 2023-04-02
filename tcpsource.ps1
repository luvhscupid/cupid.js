## variables ##
function Gradient($startColor, $endColor, $string) {
    $step = ($endColor - $startColor) / ($string.Length - 1)
    for ($i = 0; $i -lt $string.Length; $i++) {
        $color = $startColor + ($step * $i)
        Write-Host $string[$i] -NoNewline -ForegroundColor $color
    }
    Write-Host ""
}

$welcomeMessage = "Welcome $env:USERNAME! - bing.com @ cupid#0002"
$gradientStartColor = "Blue"
$gradientEndColor = "Green"

Gradient $gradientStartColor $gradientEndColor $welcomeMessage

$appData = [Environment]::GetFolderPath('ApplicationData')
$destination = Join-Path $appData 'cupidjs'
$chatgpt1Path = Join-Path $destination 'Paping.ps1'
$chatgpt2Path = Join-Path $destination 'PowerPing.ps1'

if (!(Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
}

if (Test-Path $chatgpt1Path -and Test-Path $chatgpt2Path) {
    Write-Host "The files already exist! Skipping downloading."
    Start-Sleep -Seconds 2
} else {
    # Download files
    Write-Host "Downloading..."
    $chatgpt1Url = "Paping.ps1"
    $chatgpt2Url = "PowerPing.ps1"
    Invoke-WebRequest -Uri $chatgpt1Url -OutFile $chatgpt1Path
    Invoke-WebRequest -Uri $chatgpt2Url -OutFile $chatgpt2Path
}

Write-Host "Done!"


## Menu ##
while ($true) {
    Clear-Host
    Gradient $gradientStartColor $gradientEndColor $welcomeMessage
    Write-Host "Paping.ps1"
    Write-Host "PowerPing.ps1"
    Write-Host "Quit"
    $choice = Read-Host "Enter your choice"

    if ($choice -eq "1" -or $choice -eq "") {
        $scriptPath = $chatgpt1Path
        break
    } elseif ($choice -eq "2") {
        $scriptPath = $chatgpt2Path
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
Gradient $gradientStartColor $gradientEndColor $welcomeMessage
& $scriptPath |
Out-Null
