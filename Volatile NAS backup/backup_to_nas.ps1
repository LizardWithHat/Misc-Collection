$mail_sender = 'rsnapshot@foo.bar'
$mail_reciever = 'admin@doo.bar'
$mail_head = 'Backup <Server> successful'
$message_body = "`n For more information check the rsync log on the NAS."

$console_output = <PATH>\plink.exe -ssh XXXX@XXXXX -pw XXXXX -batch '/shares/backup/backup_weekly.sh 2>&1' | Out-String
$message_body = $console_output + $message_body

if (Write-Output $console_output | Select-String -Pattern '\[ERROR\]') {
    $mail_head = 'Backup <Server> fehlerhaft!'
}


Send-MailMessage -From $mail_sender -To $mail_reciever -Subject $mail_head -Body $message_body -SmtpServer <SMPT-Server>