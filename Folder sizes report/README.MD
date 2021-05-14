This set of scripts can be modified and run in succession to build a report of folder with a file size over 40 GB and directories with a modification date thats older than 6 months of subdirectories of a specified path. The reports can then be send via a local mail server to a specified adress.

There's also a little script to compare directory names between two specified paths, which were used to avoid having two copies of a specific folder.

The "projectordner_report_sizes.ps1" uses a program named "du64.exe" which is the [disk use utility from the Microsoft Sysinternals Suite](https://docs.microsoft.com/en-us/sysinternals/downloads/du).