param(
    [string]$BuildType = "Dev"
)

$settings = lib/OGM-Common/scripts/build/OpenKNX-Build-Settings.ps1 $BuildType "IoHomecontrol" "OpenKNX-UP1-IOHC" "openknxproducer"

# This project keeps one shared application XML name for all build flavors.
$settings.releaseName = $settings.sourceName

Return $settings