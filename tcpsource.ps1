function Gradient($colors, $string) {
    $rows = 1
    $cols = $string.Length
    $step = ($colors.Length - 1) / ($cols - 1)

    for ($i = 0; $i -lt $rows; $i++) {
        for ($j = 0; $j -lt $cols; $j++) {
            $t = $j * $step
            $color1 = $colors[$j % $colors.Length]
            $color2 = $colors[($j + 1) % $colors.Length]
            $r = [Math]::Min([Math]::Max([Math]::Round($color1.R + ($color2.R - $color1.R) * $t), 0), 255)
            $g = [Math]::Min([Math]::Max([Math]::Round($color1.G + ($color2.G - $color1.G) * $t), 0), 255)
            $b = [Math]::Min([Math]::Max([Math]::Round($color1.B + ($color2.B - $color1.B) * $t), 0), 255)            
            $rgbColor = [System.Drawing.Color]::FromArgb($r, $g, $b)
            $consoleColor = $rgbColor.ToKnownColor()
            Write-Host $string[$j] -NoNewline -ForegroundColor $consoleColor
        }
        Write-Host ""
    }
}
$color1 = [System.Drawing.Color]::FromArgb(147, 112, 219)
$color2 = [System.Drawing.Color]::FromArgb(186, 85, 211)
$color3 = [System.Drawing.Color]::FromArgb(218, 112, 214)
$color4 = [System.Drawing.Color]::FromArgb(230, 143, 172)
$color5 = [System.Drawing.Color]::FromArgb(238, 174, 138)
$color6 = [System.Drawing.Color]::FromArgb(245, 222, 179)

$gradientColors = @($color1, $color2, $color3, $color4, $color5, $color6)

$welcomeMessage = "Welcome $env:USERNAME! - bing.com @ cupid#0002"
$lastColor = [System.Drawing.Color]::FromArgb(255, 255, 255)
$gradientColors += $lastColor

Gradient $gradientColors $welcomeMessage

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


## Menu ##
while ($true) {
    Gradient $gradientColors $welcomeMessage
    Write-Host "Paping.ps1"
    Write-Host "PowerPing.ps1"
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
Gradient $gradientColors $welcomeMessage
& $scriptPath |
Out-Null
