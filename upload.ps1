[CmdletBinding()]
param (
    [Parameter(HelpMessage="Init config files")]
    [switch]
    $Init=$false,
    [Parameter(HelpMessage="A profile settings to use, ex. dev, prod")]
    [String]
    $Environment=""
)

$canStart=$true # True if all requirements satified
$configFile=".ycloud_conf"
$ignoreFile=".ycloud_ignore"

# Ensure Powershell-Yaml installed

if (!(Get-Module -ListAvailable -Name PowerShell-Yaml)) {
    Write-Host "Please, install Powershell-Yaml module with this command:"
    Write-Host "Install-Module Powershell-Yaml" -ForegroundColor Green
    Write-Host ""
    $canStart=$false
}

# Ensure Yandex CLI Installed

try{
    yc -help -ErrorAction silentlycontinue | Out-Null
}
catch {
    Write-Host "Cant find YandexCloud CLI. Install with:"
    Write-Host "iex (New-Object System.Net.WebClient).DownloadString('https://storage.yandexcloud.net/yandexcloud-yc/install.ps1')" -ForegroundColor Green
    Write-Host " "
    Write-Host "Reboot, and use:"
    Write-Host "yc init" -ForegroundColor Green
    $canStart=$false
}

if (!$canStart){
    exit
}

# Initialization
if($Init){
    if(Test-Path $configFile){
        Write-Host "Config file already exists"
        Write-Host "delete ($configFile) and ($ignoreFile)"
        exit
    }
    #TODO have patterns like python, js, go
    #TODO create function if not created
    #TODO add service accounts upload
    Add-Content -Path $configFile "default: dev"
    Add-Content -Path $configFile "profiles:"
    Add-Content -Path $configFile "    dev:"
    Add-Content -Path $configFile "        function-name: my_func"
    Add-Content -Path $configFile "        runtime: python311"
    Add-Content -Path $configFile "        entrypoint: index.handler"
    Add-Content -Path $configFile "        memory: 128m"
    Add-Content -Path $configFile "        execution-timeout: 5s"
    Add-Content -Path $configFile "        folder-name: default"
    Add-Content -Path $configFile "        environment:"
    Add-Content -Path $configFile "            a: b"
    Write-Host "Created config file ($configFile)"

    $gitignoreExist=Test-Path .gitignore
    if($gitignoreExist){
        $gitignoreHasConfigFile=Select-String -Path .gitignore -Pattern $configFile -SimpleMatch -Quiet
        $gitignoreHasIgnoreFile=Select-String -Path .gitignore -Pattern $ignoreFile -SimpleMatch -Quiet
    } else{
        $gitignoreHasConfigFile=$false
        $gitignoreHasIgnoreFile=$false
    }
    $createNewLine=!$gitignoreHasConfigFile -or !$gitignoreHasIgnoreFile
    if($createNewLine -and $gitignoreExist){
        #TODO we can check the last symbol in file, if wee need to add newstring
        Add-Content -Path .gitignore '' # ensure newline
    }
    if(!$gitignoreExist -or !$gitignoreHasIgnoreFile)
    {
        Add-Content -Path .gitignore $ignoreFile
    }
    if(!$gitignoreExist -or !$gitignoreHasCongigFile)
    {
        Add-Content -Path .gitignore $congifFile
    }

    Add-Content -Path $ignoreFile $configFile
    Add-Content -Path $ignoreFile $ignoreFile
    Add-Content -Path $ignoreFile .gitignore
    Write-Host "Created upload ignore file($ignoreFile)"


    Add-Content -Path .gitignore $configFile
    Write-Host "Added ($configFile) and ($ignoreFile) to .gitignore"
    exit


}

if(!(Test-Path $configFile)){
    Write-Host "Cant find config file"
    Write-Host "Run this script with `-Init` flag"
    exit
}

#Main upload stuff

$config= Get-Content $configFile | ConvertFrom-Yaml

if("" -eq $Environment){
    $Environment=$config.default
}
Write-Host "Using Profile [$Environment]"

$settings=$config.profiles[$Environment]

$special_params=('environment')

$runString='yc serverless function version create'
foreach($parameter in $settings.GetEnumerator()){
    if($special_params.Contains($parameter.Name)){
        continue # needs special attento this field
    }
    $runString+=" --$($parameter.Name) $($parameter.Value)"
}

#convert evn variables to string
$envString=$settings.environment.keys | ForEach-Object {"$_=$($settings.environment[$_])"} | join-string -separator ',' #making env_string
$runString+=" --environment $envString"


#Zipping
$ignored=Get-Content $ignoreFile
$ignored+=$MyInvocation.InvocationName # this script
$zipfile="archive$(New-Guid).zip"

Get-ChildItem -Exclude $ignored | Compress-Archive -DestinationPath $zipfile


#Uploading
$runString+=" --source-path $zipfile"
write-Host $runString
Invoke-Expression $runString

Remove-Item $zipfile

#Make public in web if needed