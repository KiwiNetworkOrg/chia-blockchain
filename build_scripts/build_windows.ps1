# $env:path should contain a path to editbin.exe and signtool.exe

$ErrorActionPreference = "Stop"

mkdir build_scripts\win_build
Set-Location -Path ".\build_scripts\win_build" -PassThru

git status

Write-Output "   ---"
Write-Output "curl miniupnpc"
Write-Output "   ---"
Invoke-WebRequest -Uri "https://pypi.chia.net/simple/miniupnpc/miniupnpc-2.2.2-cp39-cp39-win_amd64.whl" -OutFile "miniupnpc-2.2.2-cp39-cp39-win_amd64.whl"
Write-Output "Using win_amd64 python 3.9 wheel from https://github.com/miniupnp/miniupnp/pull/475 (2.2.0-RC1)"
Write-Output "Actual build from https://github.com/miniupnp/miniupnp/commit/7783ac1545f70e3341da5866069bde88244dd848"
If ($LastExitCode -gt 0){
    Throw "Failed to download miniupnpc!"
}
else
{
    Set-Location -Path - -PassThru
    Write-Output "miniupnpc download successful."
}

Write-Output "   ---"
Write-Output "Create venv - python3.9 is required in PATH"
Write-Output "   ---"
python -m venv venv
. .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install wheel pep517
pip install pywin32
pip install pyinstaller==4.2
pip install setuptools_scm

Write-Output "   ---"
Write-Output "Get KIWI_INSTALLER_VERSION"
# The environment variable KIWI_INSTALLER_VERSION needs to be defined
$env:KIWI_INSTALLER_VERSION = python .\build_scripts\installer-version.py -win

if (-not (Test-Path env:KIWI_INSTALLER_VERSION)) {
  $env:KIWI_INSTALLER_VERSION = '0.0.0'
  Write-Output "WARNING: No environment variable KIWI_INSTALLER_VERSION set. Using 0.0.0"
  }
Write-Output "Kiwi Version is: $env:KIWI_INSTALLER_VERSION"
Write-Output "   ---"

Write-Output "   ---"
Write-Output "Build kiwi-blockchain wheels"
Write-Output "   ---"
pip wheel --use-pep517 --extra-index-url https://pypi.chia.net/simple/ -f . --wheel-dir=.\build_scripts\win_build .

Write-Output "   ---"
Write-Output "Install kiwi-blockchain wheels into venv with pip"
Write-Output "   ---"

Write-Output "pip install miniupnpc"
Set-Location -Path ".\build_scripts" -PassThru
pip install --no-index --find-links=.\win_build\ miniupnpc
# Write-Output "pip install setproctitle"
# pip install setproctitle==1.2.2

Write-Output "pip install kiwi-blockchain"
pip install --no-index --find-links=.\win_build\ kiwi-blockchain

Write-Output "   ---"
Write-Output "Use pyinstaller to create kiwi .exe's"
Write-Output "   ---"
$SPEC_FILE = (python -c 'import kiwi; print(kiwi.PYINSTALLER_SPEC_PATH)') -join "`n"
pyinstaller --log-level INFO $SPEC_FILE

Write-Output "   ---"
Write-Output "Copy kiwi executables to kiwi-blockchain-gui\"
Write-Output "   ---"
Copy-Item "dist\daemon" -Destination "..\kiwi-blockchain-gui\" -Recurse
Set-Location -Path "..\kiwi-blockchain-gui" -PassThru

git status

Write-Output "   ---"
Write-Output "Prepare Electron packager"
Write-Output "   ---"
$Env:NODE_OPTIONS = "--max-old-space-size=3000"
npm install --save-dev electron-winstaller
npm install -g electron-packager
npm install
npm audit fix

git status

Write-Output "   ---"
Write-Output "Electron package Windows Installer"
Write-Output "   ---"
npm run build
If ($LastExitCode -gt 0){
    Throw "npm run build failed!"
}

Write-Output "   ---"
Write-Output "Increase the stack for kiwi command for (kiwi plots create) kiwipos limitations"
# editbin.exe needs to be in the path
editbin.exe /STACK:8000000 daemon\kiwi.exe
Write-Output "   ---"

$packageVersion = "$env:KIWI_INSTALLER_VERSION"
$packageName = "Kiwi-$packageVersion"

Write-Output "packageName is $packageName"

Write-Output "   ---"
Write-Output "electron-packager"
electron-packager . Kiwi --asar.unpack="**\daemon\**" --overwrite --icon=.\src\assets\img\kiwi.ico --app-version=$packageVersion
Write-Output "   ---"

Write-Output "   ---"
Write-Output "node winstaller.js"
node winstaller.js
Write-Output "   ---"

git status

If ($env:HAS_SECRET) {
   Write-Output "   ---"
   Write-Output "Add timestamp and verify signature"
   Write-Output "   ---"
   signtool.exe timestamp /v /t http://timestamp.comodoca.com/ .\release-builds\windows-installer\KiwiSetup-$packageVersion.exe
   signtool.exe verify /v /pa .\release-builds\windows-installer\KiwiSetup-$packageVersion.exe
   }   Else    {
   Write-Output "Skipping timestamp and verify signatures - no authorization to install certificates"
}

git status

Write-Output "   ---"
Write-Output "Windows Installer complete"
Write-Output "   ---"
