$pyinstallerCommand = "pyinstaller main.py --onefile --name 'Anti-AFK' --icon=icon.ico"

Write-Output "Running build command. Please wait..."
try {
    Invoke-Expression $pyinstallerCommand
}
catch {
    Write-Error "Build command failed: $_"
    exit 1
}

$distDir = ".\dist"
$filesToCopy = @("start.png", "stop.png", "quit.png", "logo.png", "icon.ico", "config.json")
foreach ($file in $filesToCopy) {
    $srcPath = ".\$file"
    $dstPath = "$distDir\$file"
    try {
        Copy-Item -Path $srcPath -Destination $dstPath -Force -ErrorAction Stop
    }
    catch {
        Write-Error ("Failed to copy {0}: {1}" -f $file, $_)
        exit 1
    }
}

Write-Output "Build completed successfully."

$buildDir = ".\build"
if (Test-Path $buildDir -PathType Container) {
    Remove-Item -Path $buildDir -Recurse -Force
}

$specFile = "FFXIV Anti-AFK.spec"
if (Test-Path $specFile -PathType Leaf) {
    Remove-Item -Path $specFile -Force
}

$configFile = ".\dist\config.json"
$configContent = '{"key": "ctrl"}'
$configContent | Set-Content -Path $configFile -Force

Write-Output "Removed old files."
