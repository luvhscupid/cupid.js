$localver = "3.0"
$url = "https://raw.githubusercontent.com/luvhscupid/cupid.js/main/tcpsource.ps1"
$response = Invoke-WebRequest -Uri $url
$latestver = ($response.Content -match "Version:\s*(\d+\.\d+)")[1]

if ($latestver -gt $localver) {
    Write-Host "A new version of the script is available. Latest version: $latestver"
} else {
    Write-Host "You are running the latest version of the script ($localver)"
}
