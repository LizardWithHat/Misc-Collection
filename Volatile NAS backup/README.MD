This set of script can be used to backup a folder with a linux based NAS with volatile settings. In this case the NAS in question was a WD MyCloud.
Using this, together with cygwin-rsyncd running on a windows machine if needed, an incremental backup with 4 retaining cycles is made.
The configuration file needed for this is included in the same folder, as well as a script that automatically copies the configuration file, runs the incremental backup and grants the correct access rights.

All this happens because the NAS' operating system used is not persistent and both cronjobs (that could run the application at interval) and the rsync configuration do not stay on the NAS.
Unfortunately there is no safe way to change the NAS accordingly. To work around this, the script for the backup can be triggered by a stored task from a windows computer with PLINK installed.
The backup itself is then done by the NAS itself without the windows computer having to intervene. However, the powershell script in this folder will catch the output of the backup and send it with specified e-mail settings.