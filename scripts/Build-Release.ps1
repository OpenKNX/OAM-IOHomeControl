# This script is just a template and has to be copied and modified per project
# This script should be called from .vscode/tasks.json with
#
#   scripts/Build-Release.ps1            - for Beta builds
#   scripts/Build-Release.ps1 Release    - for Release builds

# set product names, allows mapping of (devel) name in Project to a more consistent name in release
# $settings = scripts/OpenKNX-Build-Settings.ps1

# execute generic pre-build steps
lib/OGM-Common/scripts/setup/reusable/Build-Release-Preprocess.ps1 $args[0]
if (!$?) { exit 1 }

# build firmware based on generated headerfile
# the following build steps are project specific and must be adopted accordingly
lib/OGM-Common/scripts/setup/reusable/Build-Step.ps1 release_OpenKNX_XIAO_S3_SX1262_TP firmware-OpenKNX-XIAO-S3-SX1262-TP esp32-tp
if (!$?) { exit 1 }

lib/OGM-Common/scripts/setup/reusable/Build-Step.ps1 release_OpenKNX_XIAO_S3_SX1262_IP firmware-OpenKNX-XIAO-S3-SX1262-IP esp32-ip
if (!$?) { exit 1 }

lib/OGM-Common/scripts/setup/reusable/Build-Step.ps1 release_OpenKNX_REG1_ESP_V00_11_SX1276_TP firmware-OpenKNX-REG1-ESP-V00-11-SX1276-TP esp32-tp
if (!$?) { exit 1 }

lib/OGM-Common/scripts/setup/reusable/Build-Step.ps1 release_OpenKNX_REG1_ESP_V00_11_SX1276_IP firmware-OpenKNX-REG1-ESP-V00-11-SX1276-IP esp32-ip
if (!$?) { exit 1 }

# execute generic post-build steps
lib/OGM-Common/scripts/setup/reusable/Build-Release-Postprocess.ps1 $args[0]
if (!$?) { exit 1 }