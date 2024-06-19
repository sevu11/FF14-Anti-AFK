$pyinstallerCommand = "pyinstaller main.py --onefile --name 'Anti-AFK' --icon=assets/icon.ico"

Write-Output "Running PyInstaller command. Please wait..."
try {
    Invoke-Expression $pyinstallerCommand
}
catch {
    Write-Error "PyInstaller command failed: $_"
    exit 1
}

$distDir = ".\dist"
$assetsDir = Join-Path $distDir "assets"

if (-not (Test-Path $assetsDir -PathType Container)) {
    New-Item -ItemType Directory -Path $assetsDir | Out-Null
    Write-Output "Created '$assetsDir'."
}

$filesToCopy = @("start.png", "stop.png", "quit.png", "logo.png")

foreach ($file in $filesToCopy) {
    $srcPath = Join-Path ".\assets" $file
    $dstPath = Join-Path $assetsDir $file
    if (Test-Path $srcPath -PathType Leaf) {
        Copy-Item -Path $srcPath -Destination $dstPath -Force -ErrorAction Stop
        Write-Output "Copied '$srcPath' to '$dstPath'."
    }
    else {
        Write-Error "File '$file' not found in '.\assets'. Skipping copy."
    }
}

$configFileSrc = ".\config.json"
if (Test-Path $configFileSrc -PathType Leaf) {
    $configFileDst = Join-Path $distDir "config.json"
    Copy-Item -Path $configFileSrc -Destination $configFileDst -Force -ErrorAction Stop
    Write-Output "Copied 'config.json' to '$configFileDst'."
}
else {
}

$buildDir = ".\build"
if (Test-Path $buildDir -PathType Container) {
    Remove-Item -Path $buildDir -Recurse -Force
}

$specFile = "Anti-AFK.spec"
if (Test-Path $specFile -PathType Leaf) {
    Remove-Item -Path $specFile -Force
}

$buildDirDst = ".\build"
if (Test-Path $buildDirDst -PathType Container) {
    Remove-Item -Path $buildDirDst -Recurse -Force
}
Move-Item -Path $distDir -Destination $buildDirDst -Force

Write-Output "Build process completed successfully."
