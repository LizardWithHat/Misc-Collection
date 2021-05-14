cp /shares/backup/rsnapshot.conf /etc/rsnapshot.conf
RSYNC_PASSWORD="XXXXXXXXXXXXXXXXXX" /usr/sbin/rsnapshot weekly

chown -R sicherung:share /shares/backup/weekly.0
