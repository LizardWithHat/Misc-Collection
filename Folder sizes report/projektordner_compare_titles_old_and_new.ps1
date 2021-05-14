$FolderOldProjects = Get-ChildItem -Attributes Directory -Path "\\XXXX\YYYY" -Name
$FolderNewProjects = Get-ChildItem -Attributes Directory -Path "\\XXXX\ZZZZ" -Name

Compare-Object $FolderNewProjects $FolderOldProjects -IncludeEqual -ExcludeDifferent | Select-Object -Property InputObject | Select -ExpandProperty InputObject  | Out-File -FilePath C:\Users\m.betcher\Documents\project_dir_same_names_old_new.txt -Encoding utf8