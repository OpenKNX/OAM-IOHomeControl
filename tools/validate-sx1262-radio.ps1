[CmdletBinding()]
param(
    [string]$Environment = "develop_OpenKNX_XIAO_S3_SX1262_IP",
    [Parameter(Mandatory = $true)]
    [string]$Port,
    [int]$Baud = 115200,
    [switch]$Upload,
    [ValidateSet("Auto", "Baseline", "FullIp")]
    [string]$Profile = "Auto",
    [int]$SweepIterations = 2,
    [int]$SoakSeconds = 2
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Resolve-ValidationProfile
{
    param(
        [string]$RequestedProfile,
        [string]$TargetEnvironment
    )

    if ($RequestedProfile -ne "Auto")
    {
        return $RequestedProfile
    }

    if ($TargetEnvironment -match "_IP(?:$|_)")
    {
        return "FullIp"
    }

    return "Baseline"
}

function Read-UntilIdle
{
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.Ports.SerialPort]$Serial,
        [int]$MinMs,
        [int]$IdleMs,
        [int]$MaxMs
    )

    $builder = [System.Text.StringBuilder]::new()
    $start = Get-Date
    $lastData = $start

    while ($true)
    {
        Start-Sleep -Milliseconds 100

        $text = $Serial.ReadExisting()
        if (-not [string]::IsNullOrEmpty($text))
        {
            [void]$builder.Append($text)
            $lastData = Get-Date
            Write-Host $text -NoNewline
        }

        $elapsed = ((Get-Date) - $start).TotalMilliseconds
        $idle = ((Get-Date) - $lastData).TotalMilliseconds
        if ($elapsed -ge $MinMs -and $idle -ge $IdleMs)
        {
            break
        }

        if ($elapsed -ge $MaxMs)
        {
            break
        }
    }

    return $builder.ToString()
}

function Invoke-ValidationStep
{
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.Ports.SerialPort]$Serial,
        [Parameter(Mandatory = $true)]
        [System.Text.StringBuilder]$LogBuilder,
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Step
    )

    Write-Host ">>> $($Step.Command)"
    [void]$LogBuilder.AppendLine(">>> $($Step.Command)")

    $Serial.Write("$($Step.Command)`r`n")
    Start-Sleep -Milliseconds 200

    $output = Read-UntilIdle -Serial $Serial -MinMs $Step.MinMs -IdleMs $Step.IdleMs -MaxMs $Step.MaxMs
    if ([string]::IsNullOrEmpty($output))
    {
        Write-Host "[no response]"
        [void]$LogBuilder.AppendLine("[no response]")
    }
    else
    {
        [void]$LogBuilder.Append($output)
        if (-not $output.EndsWith("`n"))
        {
            [void]$LogBuilder.AppendLine()
        }
    }

    return $output
}

function Assert-ExpectedTokens
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$Output,
        [Parameter(Mandatory = $true)]
        [string[]]$Tokens,
        [Parameter(Mandatory = $true)]
        [string]$Context,
        [Parameter(Mandatory = $true)]
        [string]$LogPath
    )

    $missingTokens = @($Tokens | Where-Object { $Output -notmatch [Regex]::Escape($_) })
    if ($missingTokens.Count -gt 0)
    {
        throw "Validation incomplete for $Context. Missing tokens: $($missingTokens -join ', '). Log: $LogPath"
    }
}

function Assert-ExchangeSummary
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$Output,
        [Parameter(Mandatory = $true)]
        [string]$Context,
        [Parameter(Mandatory = $true)]
        [string]$LogPath
    )

    $summaryMatch = [Regex]::Match($Output, 'tx=(?<tx>\d+)\s+ok=(?<ok>\d+)\s+fail=(?<fail>\d+)\s+timeout=(?<timeout>\d+)')
    if (-not $summaryMatch.Success)
    {
        throw "Validation incomplete for $Context. Missing tx/ok/fail/timeout summary. Log: $LogPath"
    }

    $tx = [int]$summaryMatch.Groups['tx'].Value
    $ok = [int]$summaryMatch.Groups['ok'].Value
    $fail = [int]$summaryMatch.Groups['fail'].Value
    $timeout = [int]$summaryMatch.Groups['timeout'].Value

    if ($tx -le 0 -or $ok -ne $tx -or $fail -ne 0 -or $timeout -ne 0)
    {
        throw "Validation failed for $Context. Observed tx=$tx ok=$ok fail=$fail timeout=$timeout. Log: $LogPath"
    }
}

if ($Upload)
{
    pio run -e $Environment -t upload
}

$artifactDir = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\artifacts"))
New-Item -ItemType Directory -Force -Path $artifactDir | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logPath = Join-Path $artifactDir "sx1262-radio-$timestamp.log"
$validationProfile = Resolve-ValidationProfile -RequestedProfile $Profile -TargetEnvironment $Environment

if ($validationProfile -eq "FullIp")
{
    $steps = @(
        [pscustomobject]@{ Name = "Selftest"; Command = "iohc proto selftest"; MinMs = 500; IdleMs = 700; MaxMs = 8000 },
        [pscustomobject]@{ Name = "RadioBaseline"; Command = "iohc radio"; MinMs = 500; IdleMs = 700; MaxMs = 5000 },
        [pscustomobject]@{ Name = "RadioRaw"; Command = "iohc radio raw"; MinMs = 500; IdleMs = 700; MaxMs = 5000 },
        [pscustomobject]@{ Name = "TxTest"; Command = "iohc radio txtest"; MinMs = 1000; IdleMs = 900; MaxMs = 8000 },
        [pscustomobject]@{ Name = "Sweep"; Command = "iohc radio sweep $SweepIterations"; MinMs = 2000; IdleMs = 1200; MaxMs = 15000 },
        [pscustomobject]@{ Name = "Soak"; Command = "iohc radio soak $SoakSeconds"; MinMs = 3000; IdleMs = 1200; MaxMs = 15000 },
        [pscustomobject]@{ Name = "RadioFinal"; Command = "iohc radio"; MinMs = 500; IdleMs = 700; MaxMs = 5000 }
    )
}
else
{
    $steps = @(
        [pscustomobject]@{ Name = "RadioBaseline"; Command = "iohc radio"; MinMs = 500; IdleMs = 700; MaxMs = 5000 },
        [pscustomobject]@{ Name = "RadioRaw"; Command = "iohc radio raw"; MinMs = 500; IdleMs = 700; MaxMs = 5000 }
    )
}

$serial = [System.IO.Ports.SerialPort]::new(
    $Port,
    $Baud,
    [System.IO.Ports.Parity]::None,
    8,
    [System.IO.Ports.StopBits]::One)
$serial.NewLine = "`r`n"
$serial.ReadTimeout = 250
$serial.WriteTimeout = 500
$serial.DtrEnable = $true
$serial.RtsEnable = $true

try
{
    $results = @{}
    $logBuilder = [System.Text.StringBuilder]::new()
    [void]$logBuilder.AppendLine("Validation profile: $validationProfile")
    [void]$logBuilder.AppendLine("Environment: $Environment")
    [void]$logBuilder.AppendLine("Port: $Port")

    $serial.Open()
    Start-Sleep -Milliseconds 1500

    $boot = $serial.ReadExisting()
    if (-not [string]::IsNullOrEmpty($boot))
    {
        Write-Host $boot -NoNewline
        [void]$logBuilder.Append($boot)
        if (-not $boot.EndsWith("`n"))
        {
            [void]$logBuilder.AppendLine()
        }
    }

    foreach ($step in $steps)
    {
        $results[$step.Name] = Invoke-ValidationStep -Serial $serial -LogBuilder $logBuilder -Step $step
    }

    $joined = $logBuilder.ToString()
    $joined | Set-Content -Path $logPath -Encoding UTF8

    if ($joined -match "Device is not Configured")
    {
        throw "Validation blocked. The target booted on $Port, but the io-homecontrol console is unavailable until KNX settings are configured in ETS and the device is power-cycled. Log: $logPath"
    }

    if ($joined -match "iohc .*: command not found")
    {
        throw "Validation blocked. The target answered on $Port, but one or more expected iohc commands are unavailable on this firmware image. Log: $logPath"
    }

    $radioOutput = $results['RadioBaseline']
    if ($results.ContainsKey('RadioFinal'))
    {
        $radioOutput = $radioOutput + "`n" + $results['RadioFinal']
    }

    $requiredTokens = @("initDev", "devErr", "tcxo", "rf")
    Assert-ExpectedTokens -Output $radioOutput -Tokens $requiredTokens -Context "radio health" -LogPath $logPath

    if ($results['RadioRaw'] -notmatch "sync=57FD99")
    {
        throw "Validation incomplete. Expected standard-mode SX1262 chip sync remap sync=57FD99 was not observed. Log: $logPath"
    }

    if ($validationProfile -eq "FullIp")
    {
        $selftestMatch = [Regex]::Match($results['Selftest'], '(?<passed>\d+)\/(?<total>\d+) checks passed')
        if (-not $selftestMatch.Success)
        {
            throw "Validation incomplete. Missing selftest success summary. Log: $logPath"
        }

        if ([int]$selftestMatch.Groups['passed'].Value -ne [int]$selftestMatch.Groups['total'].Value)
        {
            throw "Validation failed. Selftest did not pass completely. Log: $logPath"
        }

        Assert-ExpectedTokens -Output $results['TxTest'] -Tokens @("done=1", "irq=0x0001", "txSt=0x62", "devErrNow=0x0000") -Context "txtest" -LogPath $logPath
        Assert-ExchangeSummary -Output $results['Sweep'] -Context "radio sweep" -LogPath $logPath
        Assert-ExchangeSummary -Output $results['Soak'] -Context "radio soak" -LogPath $logPath
    }

    Write-Host "Validation log written to $logPath"
}
finally
{
    if ($serial.IsOpen)
    {
        $serial.Close()
    }

    $serial.Dispose()
}