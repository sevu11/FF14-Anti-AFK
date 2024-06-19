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
        Write-Error "Failed to copy $file: $_"
        exit 1
    }
}

Write-Output "Build completed successfully."