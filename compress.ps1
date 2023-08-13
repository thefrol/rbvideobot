Get-ChildItem -Path . -Exclude .*,*.ps1,_*,__* | Compress-Archive -DestinationPath archive.zip -Force
