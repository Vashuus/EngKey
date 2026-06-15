# EngKey launcher - Windows (PowerShell, autocontenido)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
python engkey.py
