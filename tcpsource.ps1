$localver = "3.0"
$url = "https://github.com/luvhscupid/cupid.js/releases/tag/cupidjs"
$response = Invoke-WebRequest -Uri $url
$latestver = ($response.Content -match "Version:\s*(\d+\.\d+)")[1]

if ($latestver -gt $localver) {
    Write-Host "A new version of the script is available. Latest version: $latestver"
} else {
    Write-Host "You are running the latest version of the script ($localver)"
}
