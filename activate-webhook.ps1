[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $Environment=$null,
    [Parameter()]
    [switch]
    $Init,
    [Parameter()]
    [switch]
    $Delete
)

$configFile='.webhook'

# Ensure Powershell-Yaml installed

if (!(Get-Module -ListAvailable -Name PowerShell-Yaml)) {
    Write-Host "Please, install Powershell-Yaml module with this command:"
    Write-Host "Install-Module Powershell-Yaml" -ForegroundColor Green
    Write-Host ""
    exit
}

#GoGo

if($Init){
    if(Test-Path $configFile){
        Write-Host "Config file $configFile already created. Delete it manually if needed"
    }
    Add-Content -Path $configFile "default: dev"
    Add-Content -Path $configFile "profiles:"
    Add-Content -Path $configFile "    dev:"
    Add-Content -Path $configFile "        token: 123123..."
    Add-Content -Path $configFile "        url: https://your_url"
    Add-Content -Path $configFile "    prod:"
    Add-Content -Path $configFile "        token: 123123..."
    Add-Content -Path $configFile "        url: https://your_url"

    Write-Host "Config file created. Now edit $configFile"
    
    Add-Content -Path .gitignore $configFile
    exit
}

if(!(Test-Path $configFile)){
    Write-Host "Config file not found, run this with `"-Init`""
    exit
}

$config=Get-Content $configFile | ConvertFrom-Yaml

if(!$Environment){
    $Environment=$config.default
}
if(!$Delete){
    $resp=Invoke-RestMethod "https://api.telegram.org/bot$($config.profiles[$Environment].token)/setWebhook?url=$($config.profiles[$Environment].url)"
} else{
    $resp=Invoke-RestMethod "https://api.telegram.org/bot$($config.profiles[$Environment].token)/setWebhook?remove"
}


if(!$?){
    Write-Host "Not done. Some connection issues. Try again later."
}

if($resp.ok){
    Write-Host "Success!!!" 
} else{
    Write-Host "Error. Webhook not set"
}

Write-Host $resp.description


