Get-ChildItem -Path <PATH> -Directory | 
    Select-Object -Property Name, @{Label='LastWriteInside'; Expression={ 
        ($_ | Get-ChildItem -Recurse -Force|
         Sort-object -property LastWriteTime|
         Select-Object -expandproperty lastwritetime -Last 1)
        }} |
    Sort-Object -Property LastWriteInside |
Export-Csv -Path C:\XXXXX\project_dir_lastmodified.csv -NoTypeInformation