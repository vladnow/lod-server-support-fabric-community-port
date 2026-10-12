param(
    [string]$JavaHome = $env:JAVA_HOME,
    [string]$GradleExecutable,
    [switch]$Offline,
    [switch]$GameTests
)
$ErrorActionPreference = 'Stop'
if (!$JavaHome -or !(Test-Path -LiteralPath (Join-Path $JavaHome 'bin/javac.exe'))) {
    throw 'Specify a JDK 25 directory using -JavaHome or JAVA_HOME.'
}
$env:JAVA_HOME = $JavaHome
$env:PATH = "$JavaHome\bin;$env:PATH"
$taskStage = Join-Path $env:TEMP 'lss-port-263'
$taskProject = Join-Path $taskStage ('build-' + [Guid]::NewGuid().ToString('N'))
$env:GRADLE_USER_HOME = Join-Path $taskStage 'gradle-home'
New-Item -ItemType Directory -Path $taskProject,$env:GRADLE_USER_HOME,(Join-Path $PSScriptRoot 'dist'),(Join-Path $PSScriptRoot 'verification') -Force | Out-Null
if ($taskProject -match '[^\x00-\x7F]') { throw 'TEMP must point to a Latin-only path for Gradle worker compatibility.' }
# Copy source only. No user worlds or launcher profiles are touched.
$taskExcluded = @('.git','.gradle','build','dist','verification','.tools','lod-server-support-main','__pycache__')
function Copy-PortSources([string]$TaskSource, [string]$TaskDestination) {
    New-Item -ItemType Directory -Path $TaskDestination -Force | Out-Null
    Get-ChildItem -LiteralPath $TaskSource -Force | Where-Object { $_.Name -notin $taskExcluded } | ForEach-Object {
        $taskTarget = Join-Path $TaskDestination $_.Name
        if ($_.PSIsContainer) { Copy-PortSources $_.FullName $taskTarget }
        else { Copy-Item -LiteralPath $_.FullName -Destination $taskTarget -Force }
    }
}
Copy-PortSources $PSScriptRoot $taskProject
if (!$GradleExecutable) { $GradleExecutable = Join-Path $taskProject 'gradlew.bat' }
$taskArgs = @(':fabric:build',':common:test','--no-daemon','--console=plain','--max-workers=2')
if ($GameTests) { $taskArgs += ':fabric:runGameTest' }
if ($Offline) { $taskArgs += '--offline' }
Push-Location $taskProject
try {
    & $GradleExecutable @taskArgs *> (Join-Path $PSScriptRoot 'verification/build.log')
    $taskExit = $LASTEXITCODE
    Get-Content -LiteralPath (Join-Path $PSScriptRoot 'verification/build.log') -Tail 40
    if ($taskExit -ne 0) { throw "Build failed (exit $taskExit). See verification/build.log." }
    $taskVersion = ((Get-Content gradle.properties | Where-Object { $_ -match '^mod_version=' }) -split '=',2)[1].Trim()
    foreach ($taskName in @("lod-server-support-fabric-$taskVersion.jar","voxy-server-side-fabric-$taskVersion.jar")) {
        Copy-Item -LiteralPath (Join-Path 'fabric/build/libs' $taskName) -Destination (Join-Path $PSScriptRoot "dist/$taskName") -Force
    }
    foreach ($taskModule in @('common','fabric')) {
        $taskResults = Join-Path $taskProject "$taskModule/build/test-results/test"
        if (Test-Path -LiteralPath $taskResults) { Copy-Item -LiteralPath $taskResults -Destination (Join-Path $PSScriptRoot "verification/$taskModule-tests") -Recurse -Force }
    }
    $taskHashes = Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'dist') -Filter '*.jar' | ForEach-Object {
        $taskHash = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
        "$($taskHash.Hash.ToLower())  $($_.Name)"
    }
    [IO.File]::WriteAllLines((Join-Path $PSScriptRoot 'dist/SHA256SUMS.txt'),$taskHashes,[Text.UTF8Encoding]::new($false))
    Write-Output "Prepared Fabric artifacts in $(Join-Path $PSScriptRoot 'dist')."
} finally { Pop-Location }
