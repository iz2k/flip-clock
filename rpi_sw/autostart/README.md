# Autostart flip-clock as service
Use the following properties in your systemd service unit file:

StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=<your program identifier> # without any quote
Then, assuming your distribution is using rsyslog to manage syslogs, create a file in /etc/rsyslog.d/<new_file>.conf with the following content:

if $programname == '<your program identifier>' then /path/to/log/file.log
& stop
Now make the log file writable by syslog:

# ls -alth /var/log/syslog 
-rw-r----- 1 syslog adm 439K Mar  5 19:35 /var/log/syslog
# chown syslog:adm /path/to/log/file.log
Restart rsyslog (sudo systemctl restart rsyslog) and enjoy! Your program stdout/stderr will still be available through journalctl (sudo journalctl -u <your program identifier>) but they will also be available in your file of choice.